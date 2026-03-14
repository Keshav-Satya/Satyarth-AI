import streamlit as st
import os
import base64
from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun
import google.generativeai as genai
from PIL import Image

# # 1. Page Configuration
st.set_page_config(page_title="Satyarth-AI | Forensic Engine", page_icon="🛡️", layout="wide")

# # 2. Cyber-Security UI (Indigo Theme)
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); color: #f1f5f9; }
    [data-testid="stWidgetLabel"] p { font-size: 1.25rem !important; font-weight: 700 !important; color: #38bdf8 !important; }
    .report-card {
        background: rgba(30, 41, 59, 0.85); backdrop-filter: blur(15px);
        border-radius: 20px; padding: 25px; border: 1px solid rgba(56, 189, 248, 0.3);
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.6); margin-top: 20px; color: white;
    }
    .main-title {
        background: linear-gradient(to right, #38bdf8, #818cf8);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-size: 4rem; font-weight: 900; text-align: center;
    }
    .stButton>button {
        background: linear-gradient(45deg, #0284c7, #4f46e5); color: white;
        padding: 14px 30px; border-radius: 12px; font-weight: 700; width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# # 3. API Keys Verification
if "SAMBANOVA_API_KEY" not in st.secrets or "GOOGLE_API_KEY" not in st.secrets:
    st.error("Sir, please Secrets mein Keys check karein!")
    st.stop()

# # 4. Engine Setup
text_llm = LLM(
    model="sambanova/Meta-Llama-3.3-70B-Instruct", 
    base_url="https://api.sambanova.ai/v1",
    api_key=st.secrets["SAMBANOVA_API_KEY"],
    temperature=0.2 # Thoda sa temperature badhaya for better analysis depth
)

@tool('search_tool')
def search_tool(query: str):
    """Deep search tool for news verification."""
    search = DuckDuckGoSearchRun()
    # Increase context to 500 chars for match results/highlights
    return search.run(query)[:500]

# # 5. Sidebar
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #38bdf8;'>🛡️ Satyarth-AI</h2>", unsafe_allow_html=True)
    st.metric("Mode", "Forensic Analyst 📍")
    st.info("📡 SambaNova: Connected")
    st.info("💠 Gemini Vision: Ready")
    st.write("---")
    st.markdown("Developed by **Team Future Flux**")

# # 6. Header
st.markdown('<h1 class="main-title">SATYARTH-AI</h1>', unsafe_allow_html=True)
st.write("---")

tab1, tab2 = st.tabs(["🔍 Text Verification", "🔬 Image Investigation"])

# --- TAB 1: Text ---
with tab1:
    col1, col2 = st.columns([3, 1])
    with col1: news_topic = st.text_input("News Headline Daalein 👇")
    with col2: location = st.text_input("Location 📍", value="Global")

    if st.button("🚀 START DEEP FORENSIC ANALYSIS"):
        if news_topic:
            with st.status("🕵️ Investigating Context & Evidence...", expanded=True) as status:
                # Optimized Agents with Hinglish focus and NO Scorecard
                scout = Agent(
                    role='Forensic Research Agent',
                    goal=f'Verify {news_topic} in {location}. Dhyan rahe ki match dates, winners aur official ICC reports check karein.',
                    backstory="Aap ek expert investigator hain jo deep web se specific match details aur official results nikaalte hain. Detailed facts collect karein.",
                    tools=[search_tool], llm=text_llm, verbose=True
                )
                analyst = Agent(
                    role='Expert News Analyst',
                    goal='Create a detailed analysis report in HINGLISH. Do NOT include any Score Card or numeric rating.',
                    backstory="""Aapko results ko Hinglish (Hindi + English) mein explain karna hai. 
                    Evidence ko breakdown karein aur clear verdict dein ki news Real hai ya Fake. 
                    Strictly follow: No Scorecard, Only Detailed Reasoning.""",
                    llm=text_llm, verbose=True
                )

                crew = Crew(
                    agents=[scout, analyst],
                    tasks=[
                        Task(description=f"Thoroughly check news about: {news_topic} in {location}. Match results aur historical records compare karein.", agent=scout, expected_output="Detailed list of facts and links."),
                        Task(description="Create a comprehensive analysis report in Hinglish. Summarize findings, give a verdict, and list sources at the end. DO NOT USE SCORECARDS.", agent=analyst, expected_output="Detailed Hinglish Report.")
                    ],
                    process=Process.sequential
                )
                result = crew.kickoff()
                status.update(label="Analysis Complete! ✅", state="complete")
                
                st.markdown(f'<div class="report-card"><h3>📜 Forensic Report</h3>{result.raw}</div>', unsafe_allow_html=True)
                
                if any(x in result.raw.lower() for x in ["real", "true", "sahi", "authentic"]): st.balloons()
                elif any(x in result.raw.lower() for x in ["fake", "false", "galat", "misleading"]): st.snow()
        else:
            st.warning("Sir, please headline enter karein!")

# --- TAB 2: Image ---
with tab2:
    st.markdown("### 🔬 Image Forensic Module")
    cam_toggle = st.toggle("🎥 Activate Live Camera", value=False)
    c1, c2 = st.columns(2)
    img_cam = None 
    with c1: img_file = st.file_uploader("Upload Image", type=['jpg','png','jpeg'])
    with c2: 
        if cam_toggle: img_cam = st.camera_input("Take Photo")
        else: st.info("Camera is OFF.")
    
    final_img = img_file if img_file is not None else img_cam
    if final_img is not None:
        st.image(final_img, caption="Forensic Scan Ready.", width=500)
        if st.button("🔍 RUN PIXEL ANALYSIS"):
            with st.spinner("Analyzing..."):
                try:
                    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    response = model.generate_content(["Analyze image markers. Verdict in Hinglish.", Image.open(final_img)])
                    st.markdown(f'<div class="report-card"><h3>🔬 Verdict</h3>{response.text}</div>', unsafe_allow_html=True)
                except Exception as e: st.error(f"Error: {e}")
