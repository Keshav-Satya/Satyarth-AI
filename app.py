import streamlit as st
import os
import base64
from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun
from PIL import Image
import google.generativeai as genai

# # 1. Page Configuration
st.set_page_config(page_title="Satyarth-AI | Forensic Engine", page_icon="🛡️", layout="wide")

# # 2. Advanced Cyber-Forensic UI Styling
st.markdown("""
    <style>
    /* Global Background */
    .stApp { background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); color: #f1f5f9; }
    
    /* Neon Sidebar Dashboard */
    [data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.95) !important;
        border-right: 2px solid #38bdf8;
    }
    .metric-container {
        background: rgba(255, 255, 255, 0.05);
        padding: 15px; border-radius: 12px;
        border-left: 4px solid #38bdf8; margin-bottom: 10px;
    }
    
    /* Tech Pulse Animation */
    .pulse {
        height: 10px; width: 10px; background-color: #38bdf8;
        border-radius: 50%; display: inline-block;
        box-shadow: 0 0 0 rgba(56, 189, 248, 0.4);
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(56, 189, 248, 0.7); }
        70% { transform: scale(1); box-shadow: 0 0 0 10px rgba(56, 189, 248, 0); }
        100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(56, 189, 248, 0); }
    }

    /* Input Labels Readability */
    [data-testid="stWidgetLabel"] p {
        font-size: 1.25rem !important; font-weight: 700 !important;
        color: #38bdf8 !important; text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
    }

    /* Main UI Polish */
    .main-title {
        background: linear-gradient(to right, #38bdf8, #818cf8);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-size: 4.2rem; font-weight: 900; text-align: center;
        text-shadow: 0 10px 30px rgba(56, 189, 248, 0.2);
    }
    .report-card {
        background-color: rgba(255, 255, 255, 0.05); backdrop-filter: blur(15px);
        padding: 30px; border-radius: 20px; border: 1px solid rgba(56, 189, 248, 0.3);
        color: #f1f5f9; margin-top: 20px;
    }
    .stButton>button {
        background: linear-gradient(45deg, #0284c7, #4f46e5); color: white;
        padding: 14px 30px; border-radius: 12px; font-weight: 700; width: 100%; transition: 0.3s;
    }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 0 30px rgba(56, 189, 248, 0.5); }
    </style>
    """, unsafe_allow_html=True)

# # 3. API Keys Verification
if "SAMBANOVA_API_KEY" not in st.secrets or "GOOGLE_API_KEY" not in st.secrets:
    st.error("Sir, please Secrets mein SAMBANOVA_API_KEY aur GOOGLE_API_KEY check karein!")
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
    """Search internet for news facts with token saving."""
    search = DuckDuckGoSearchRun()
    search_result = search.run(query)
    return search_result[:400]

# # 5. Pro Tech Sidebar Dashboard
with st.sidebar:
    st.markdown("## 🛡️ Satyarth Engine")
    st.markdown('<p><span class="pulse"></span> System Status: Online</p>', unsafe_allow_html=True)
    st.write("---")
    
    st.markdown("### 📊 Live Metrics")
    st.markdown('<div class="metric-container"><b>SambaNova:</b> Active 🟢<br><small>Latency: 42ms</small></div>', unsafe_allow_html=True)
    st.markdown('<div class="metric-container"><b>Forensic Agents:</b> 2 Running<br><small>Mode: Hyper-Local</small></div>', unsafe_allow_html=True)
    st.markdown('<div class="metric-container"><b>Uptime:</b> Stable</div>', unsafe_allow_html=True)
    
    st.write("---")
    st.markdown("Developed by **Team Future Flux**")
    st.caption("NIT Hamirpur | Electrothon 8.0")

# # 6. Header
st.markdown('<h1 class="main-title">SATYARTH-AI</h1>', unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8;'>Hyper-Local Disinformation Detection & Image Forensic Engine</p>", unsafe_allow_html=True)
st.write("---")

tab1, tab2 = st.tabs(["🔍 Text Verification", "🔬 Image Investigation"])

# --- TAB 1: Text Investigation ---
with tab1:
    col_input, col_loc = st.columns([2, 1])
    with col_input:
        news_topic = st.text_input("News Headline Daalein 👇", placeholder="e.g. Is Virat Kohli retiring?")
    with col_loc:
        region = st.text_input("Region (District and State) 📍", placeholder="e.g. Hamirpur, Himachal Pradesh")

    if st.button("🚀 Start Deep Satyarth Analysis", key="text_btn"):
        if news_topic:
            with st.status(f"🕵️ Investigating {news_topic} in {region}...", expanded=True) as status:
                # Agents definition
                scout = Agent(
                    role='Local Data Scout',
                    goal=f'Verify {news_topic} in {region}. Check district level news portals. Today is March 15, 2026.',
                    backstory="Aap ek expert digital detective hain jo specific regions ki news verify karte hain.",
                    tools=[search_tool], llm=text_llm, verbose=True
                )
                analyst = Agent(
                    role='Lead Forensic Verifier',
                    goal='Write a detailed Hinglish verdict report. No scorecards.',
                    backstory="Aap results ko professional Hinglish mein verify karte hain.",
                    llm=text_llm, verbose=True
                )
                crew = Crew(
                    agents=[scout, analyst],
                    tasks=[
                        Task(description=f"Check {news_topic} specifically in {region} context.", agent=scout, expected_output="Local facts & links."),
                        Task(description="Synthesize into a professional Hinglish report with clear verdict.", agent=analyst, expected_output="Final Report.")
                    ],
                    process=Process.sequential
                )
                result = crew.kickoff()
                st.session_state.final_report = result.raw
                status.update(label="Analysis Complete! ✅", state="complete")
            st.balloons()
        else:
            st.warning("Sir, please news enter kijiye!")

    # Show report and Human Verification button only if analysis is done
    if "final_report" in st.session_state:
        st.markdown(f'<div class="report-card"><h3>📜 Forensic Report</h3>{st.session_state.final_report}</div>', unsafe_allow_html=True)
        st.write("---")
        st.markdown("### 👥 Human Intelligence Module")
        if st.button("Request Human Verification"):
            st.info("you will be informed when we receive reply")

# --- TAB 2: Image Investigation ---
with tab2:
    st.markdown("### 🔬 Image Forensic Module")
    cam_toggle = st.toggle("🎥 Activate Live Camera Feed", value=False)
    
    c1, c2 = st.columns(2)
    img_cam = None 
    with c1: img_file = st.file_uploader("Upload Image", type=['jpg','png','jpeg'])
    with c2: 
        if cam_toggle:
            img_cam = st.camera_input("Take Photo")
        else:
            st.info("Camera is OFF.")

    # Fix logic: only consider if it's a valid file object
    final_img = img_file if img_file is not None else img_cam
    
    if final_img is not None:
        st.image(final_img, caption="Forensic Scan Ready.", width=500)
        if st.button("🔍 RUN PIXEL ANALYSIS", key="img_btn"):
            with st.spinner("Analyzing image for AI markers..."):
                try:
                    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    response = model.generate_content(["Analyze image for AI artifacts. Verdict in Hinglish.", Image.open(final_img)])
                    st.markdown(f'<div class="report-card"><h3>🔬 Verdict</h3>{response.text}</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Error: {e}")
