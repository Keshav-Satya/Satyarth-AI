import streamlit as st
import os
import base64
from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun
from groq import Groq
from PIL import Image
import google.generativeai as genai

# # 1. Page Configuration
st.set_page_config(page_title="Satyarth-AI | Multimodal", page_icon="🕵️", layout="wide")

# # 2. Professional UI Styling (Cyber-Security Theme)
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); color: #f1f5f9; }
    [data-testid="stWidgetLabel"] p { font-size: 1.25rem !important; font-weight: 700 !important; color: #38bdf8 !important; }
    .report-card {
        background-color: rgba(255, 255, 255, 0.05); backdrop-filter: blur(12px);
        padding: 30px; border-radius: 20px; border: 1px solid rgba(56, 189, 248, 0.3);
        color: #f1f5f9; margin-top: 20px;
    }
    .main-title { color: #38bdf8; font-size: 3.5rem; font-weight: 900; text-align: center; }
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

# # 4. Models Initialization
text_llm = LLM(
    model="sambanova/Meta-Llama-3.3-70B-Instruct", 
    base_url="https://api.sambanova.ai/v1",
    api_key=st.secrets["SAMBANOVA_API_KEY"],
    temperature=0.1
)

@tool('search_tool')
def search_tool(query: str):
    """Search internet for news facts with extreme token saving."""
    search = DuckDuckGoSearchRun()
    search_result = search.run(query)
    # Fixed Syntax Error: Square bracket closed properly
    return search_result[:300]

# --- Sidebar ---
with st.sidebar:
    st.markdown("# 🕵️ Satyarth-AI")
    st.success("✅ System: Multimodal Active")
    st.write("---")
    st.markdown("Developed by **Team Future Flux**")

# --- Header ---
st.markdown('<h1 class="main-title">SATYARTH-AI</h1>', unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Advanced Disinformation Detection & Image Forensic Engine</p>", unsafe_allow_html=True)
st.write("---")

tab1, tab2 = st.tabs(["📝 Text Verification", "📷 Image Investigation"])

# --- TAB 1: Text Investigation ---
with tab1:
    news_topic = st.text_input("Sir, kis news ka analysis karna hai?", placeholder="e.g. Is viral news real?")
    
    if st.button("🚀 Start Satyarth Analysis", type="primary"):
        if news_topic:
            with st.status("🔍 Analyzing Live Evidence...", expanded=True) as status:
                scout = Agent(
                    role='Digital Detective',
                    goal=f'Verify {news_topic}. Current date is March 15, 2026.',
                    backstory="Aap facts verify karte hain aur sources check karte hain.",
                    tools=[search_tool], llm=text_llm, verbose=True
                )
                analyst = Agent(
                    role='Forensic Analyst',
                    goal='Create a final verdict report in HINGLISH. No scorecards.',
                    backstory="Aap results ko professional Hinglish mein explain karte hain.",
                    llm=text_llm, verbose=True
                )
                crew = Crew(
                    agents=[scout, analyst],
                    tasks=[
                        Task(description=f"Check facts for: {news_topic}", agent=scout, expected_output="Facts and sources."),
                        Task(description="Write a detailed Hinglish report with a verdict.", agent=analyst, expected_output="Final Hinglish report.")
                    ],
                    process=Process.sequential
                )
                result = crew.kickoff()
                # Persistence logic: storing in session state
                st.session_state.final_report = result.raw
                status.update(label="Investigation Complete! ✅", state="complete")
            st.balloons()
        else:
            st.warning("Sir, please topic enter kijiye!")

    # Report aur Human Verification sirf tab dikhega jab report taiyar ho
    if "final_report" in st.session_state:
        st.markdown(f'<div class="report-card"><h3>📜 Forensic Report</h3>{st.session_state.final_report}</div>', unsafe_allow_html=True)
        st.write("---")
        st.markdown("### 👥 Human Intelligence Module")
        if st.button("Request Human Verification"):
            st.info("you will be informed when we receive reply")

# --- TAB 2: Image Investigation ---
with tab2:
    cam_on = st.toggle("📸 Camera Toggle", value=False)
    c1, c2 = st.columns(2)
    img_cam = None
    with c1: img_file = st.file_uploader("Upload photo", type=['jpg', 'png', 'jpeg'])
    with c2: 
        if cam_on: img_cam = st.camera_input("Take Live Photo")
        else: st.info("Camera is OFF.")

    final_img = img_file if img_file is not None else img_cam
    
    if final_img is not None:
        st.image(final_img, caption="Forensic Scan Ready.", width=400)
        if st.button("🔍 Run Image Analysis"):
            with st.spinner("Analyzing pixels..."):
                try:
                    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    response = model.generate_content(["Analyze image for AI artifacts. Verdict in Hinglish.", Image.open(final_img)])
                    st.markdown(f'<div class="report-card"><h3>🔬 Verdict</h3>{response.text}</div>', unsafe_allow_html=True)
                except Exception as e: st.error(f"Error: {e}")
