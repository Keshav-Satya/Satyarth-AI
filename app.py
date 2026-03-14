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

# # 2. Cyber-Security UI (Stable Hinglish Edition)
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

# # 4. Engine Setup (Switched to 11B for higher rate limits)
text_llm = LLM(
    model="sambanova/Llama-3.2-11B-Vision-Instruct", 
    base_url="https://api.sambanova.ai/v1",
    api_key=st.secrets["SAMBANOVA_API_KEY"],
    temperature=0.1
)

@tool('search_tool')
def search_tool(query: str):
    """Balanced search for news facts."""
    search = DuckDuckGoSearchRun()
    # 350 characters balance hai tokens aur analysis ke liye
    return search.run(query)[:350]

# # 5. Sidebar
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #38bdf8;'>🛡️ Satyarth-AI</h2>", unsafe_allow_html=True)
    st.metric("Mode", "Forensic Stability Active ✅")
    st.info("📡 SambaNova: Stable Mode")
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
            with st.status("🕵️ Investigating Evidence...", expanded=True) as status:
                # Optimized Agents: Strictly Hinglish & Detailed Analysis
                scout = Agent(
                    role='Forensic Scout',
                    goal=f'Verify {news_topic} in {location} context. Find official ICC or Govt records.',
                    backstory="Aap ek expert investigator hain. Specific dates aur results verify karein.",
                    tools=[search_tool], llm=text_llm, verbose=True
                )
                analyst = Agent(
                    role='News Analyst',
                    goal='Create a detailed analysis report in HINGLISH. No scorecards.',
                    backstory="Aap results ko Hinglish mein explain karte hain. Evidence aur clear verdict dein.",
                    llm=text_llm, verbose=True
                )

                crew = Crew(
                    agents=[scout, analyst],
                    tasks=[
                        Task(description=f"Check matches and records for: {news_topic} in {location}.", agent=scout, expected_output="Facts and links."),
                        Task(description="Write detailed Hinglish report with clear verdict and sources. Do NOT use any scores.", agent=analyst, expected_output="Detailed Hinglish Report.")
                    ],
                    process=Process.sequential
                )
                
                try:
                    result = crew.kickoff()
                    status.update(label="Analysis Complete! ✅", state="complete")
                    st.markdown(f'<div class="report-card"><h3>📜 Forensic Report</h3>{result.raw}</div>', unsafe_allow_html=True)
                    
                    if any(x in result.raw.lower() for x in ["real", "true", "sahi", "authentic"]): st.balloons()
                    elif any(x in result.raw.lower() for x in ["fake", "false", "galat", "fraud"]): st.snow()
                except Exception as e:
                    st.error("Sir, SambaNova ki limit hit ho gayi hai. 60 seconds baad phir se try karein.")
            
            st.write("---")
            if st.button("👥 Request Human Expert Verification"):
                st.info(f"Sir, humne {location} ke verified experts ko request bhej di hai! 📡")
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
