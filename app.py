import streamlit as st
import os
import base64
from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun
import google.generativeai as genai
from PIL import Image

# # 1. Page Config & High-Contrast CSS
st.set_page_config(page_title="Satyarth-AI | Forensic Engine", page_icon="🛡️", layout="wide")

st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); color: #f1f5f9; }
    
    /* Labels Readability Fix */
    [data-testid="stWidgetLabel"] p {
        font-size: 1.2rem !important; font-weight: 700 !important; color: #38bdf8 !important;
    }

    /* Glassmorphism Report Card */
    .report-card {
        background: rgba(30, 41, 59, 0.8); backdrop-filter: blur(15px);
        border-radius: 20px; padding: 25px; border: 1px solid rgba(56, 189, 248, 0.3);
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5); margin-top: 20px;
    }

    .main-title {
        background: linear-gradient(to right, #38bdf8, #818cf8);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-size: 3.5rem; font-weight: 900; text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# # 2. Models Initialization
text_llm = LLM(
    model="openai/meta-llama/Llama-3.3-70B-Instruct",
    base_url="https://api.sambanova.ai/v1",
    api_key=st.secrets["SAMBANOVA_API_KEY"],
    temperature=0.1
)

@tool('search_tool')
def search_tool(query: str):
    """Search for local and official facts."""
    search = DuckDuckGoSearchRun()
    return search.run(query)[:250]

# # 3. Sidebar Metrics
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #38bdf8;'>🛡️ Satyarth-AI</h2>", unsafe_allow_html=True)
    st.metric("System Mode", "Hyper-Local 📍")
    st.info("📡 Connection: Active")
    st.write("---")
    st.markdown("Developed by **Team Future Flux** | NIT Hamirpur")

# # 4. Main UI
st.markdown('<h1 class="main-title">SATYARTH-AI</h1>', unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8;'>Advanced Local News Verification & Image Forensics</p>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🔍 News Verification", "🔬 Image Investigation"])

with tab1:
    col1, col2 = st.columns([3, 1])
    with col1:
        news_topic = st.text_input("News Headline Daalein 👇")
    with col2:
        location = st.text_input("Location 📍", value="Global")

    if st.button("🚀 Run Deep Forensic Analysis"):
        if news_topic:
            with st.status("🕵️ Investigating Local Sources...", expanded=True) as status:
                # Agents definitions from agents.py logic
                from agents import scout_agent, analyst_agent 
                
                crew = Crew(
                    agents=[scout_agent, analyst_agent],
                    tasks=[
                        Task(description=f"Verify {news_topic} in {location} using local vendors & portals.", agent=scout_agent, expected_output="Facts & Sources"),
                        Task(description="Generate Hinglish forensic report with Credibility Score.", agent=analyst_agent, expected_output="Final Report")
                    ],
                    process=Process.sequential
                )
                result = crew.kickoff()
                status.update(label="Analysis Complete! ✅", state="complete")
                
                st.markdown(f'<div class="report-card"><h3>📜 Forensic Report</h3>{result.raw}</div>', unsafe_allow_html=True)
                
                # Animations based on verdict
                if any(x in result.raw.lower() for x in ["real", "true", "sahi"]): st.balloons()
                elif any(x in result.raw.lower() for x in ["fake", "false", "galat"]): st.snow()

            # --- Recording Recommendation: Human Verification ---
            st.write("---")
            st.markdown("### 👥 Human Intelligence Module")
            if st.button("Request Human Expert Verification (Local Vendors/Agents)"):
                st.toast("Sending request to local human agents...")
                st.info(f"Sir, humne {location} ke local vendors aur 'Human Agents' ko alert bhej diya hai. Ground reality ki report jald hi update hogi! 📡")

# --- Tab 2: Image Investigation ---
with tab2:
    st.markdown("### 📸 Image Forensic Module")
    cam_on = st.toggle("🎥 Activate Live Camera", value=False)
    up_col, cam_col = st.columns(2)
    with up_col: img_file = st.file_uploader("Upload Image", type=['jpg','png','jpeg'])
    with cam_col: cam_file = st.camera_input("Take Photo") if cam_on else st.write("Camera is OFF.")

    final_img = img_file or cam_file
    if final_img:
        st.image(final_img, caption="Forensic Scan Ready.", width=400)
        if st.button("🔍 Analyze Pixels"):
            try:
                genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(["Analyze image for AI markers. Verdict in Hinglish.", Image.open(final_img)])
                st.markdown(f'<div class="report-card"><h3>🔬 Verdict</h3>{response.text}</div>', unsafe_allow_html=True)
            except Exception as e: st.error(f"Error: {e}")
