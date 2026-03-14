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

# # 2. Ultra-High Visibility Cyber CSS
st.markdown("""
    <style>
    /* Global Background */
    .stApp { background: linear-gradient(135deg, #020617 0%, #0f172a 100%); color: #ffffff; }
    
    /* Neon Sidebar - Visibility Overhaul */
    [data-testid="stSidebar"] {
        background-color: #020617 !important;
        border-right: 3px solid #0ea5e9;
    }
    .metric-container {
        background: rgba(14, 165, 233, 0.25);
        padding: 18px; border-radius: 12px;
        border: 2px solid #38bdf8; margin-bottom: 18px;
    }
    .metric-container b { color: #ffffff !important; font-size: 1.25rem; }
    .metric-container small { color: #ffffff !important; font-weight: 900; letter-spacing: 1.2px; text-transform: uppercase; }
    
    /* Expander Text Readability (How it works) - FORCE WHITE */
    .stExpander { border: 1px solid #38bdf8 !important; background: rgba(255, 255, 255, 0.05) !important; }
    .stExpander p, .stExpander li, .stExpander span { 
        color: #ffffff !important; 
        font-weight: 700 !important; 
        font-size: 1.05rem !important; 
    }

    /* Decorated Title & Live Scanner */
    .main-title {
        background: linear-gradient(90deg, #38bdf8, #ffffff, #38bdf8);
        background-size: 200% auto;
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-size: 5rem; font-weight: 900; text-align: center;
        filter: drop-shadow(0 0 15px rgba(56, 189, 248, 0.6));
        animation: shine 3s linear infinite;
    }
    @keyframes shine { to { background-position: 200% center; } }

    .scanner {
        width: 100%; height: 4px; background: #38bdf8;
        box-shadow: 0 0 15px #38bdf8; position: relative; overflow: hidden;
        margin-bottom: 20px; border-radius: 2px;
    }
    .scanner::after {
        content: ''; display: block; width: 150px; height: 100%;
        background: #ffffff; position: absolute; animation: scan 2.5s linear infinite;
    }
    @keyframes scan { 0% { left: -150px; } 100% { left: 100%; } }

    /* GREEN Labels for Headlines & Region */
    [data-testid="stWidgetLabel"] p {
        font-size: 1.35rem !important; font-weight: 900 !important; color: #22c55e !important;
        background: rgba(34, 197, 94, 0.2); padding: 8px 18px; border-radius: 10px;
        display: inline-block; margin-bottom: 15px !important; border-left: 6px solid #22c55e;
    }

    /* BUTTON VISIBILITY FIX - FORCE TEXT TO BE VISIBLE ALWAYS */
    .stButton>button {
        color: #ffffff !important; /* Force text to white */
        font-weight: 900 !important;
        font-size: 1.1rem !important;
        border-radius: 12px !important;
        transition: 0.3s !important;
    }

    /* Main Analysis Button (Blue Gradient) */
    .text-btn-container .stButton>button {
        background: linear-gradient(45deg, #0ea5e9, #2563eb) !important;
        border: 2px solid #38bdf8 !important;
    }

    /* Human Verification Button (Vibrant Multi-color/Red) */
    .colorful-btn .stButton>button {
        background: linear-gradient(45deg, #ff0055, #4a90e2, #22c55e) !important;
        border: 2px solid #ffffff !important;
        box-shadow: 0 0 15px rgba(255, 0, 85, 0.4) !important;
    }

    /* Developer Info */
    .dev-label { color: #38bdf8 !important; font-weight: 900; font-size: 1.1rem; margin-top: 25px; }
    .email-text { color: #ffffff !important; font-weight: 800; background: #0ea5e9; padding: 6px 12px; border-radius: 6px; display: inline-block; }
    </style>
    """, unsafe_allow_html=True)

# # 3. Engine Setup
text_llm = LLM(
    model="sambanova/Meta-Llama-3.3-70B-Instruct", 
    base_url="https://api.sambanova.ai/v1",
    api_key=st.secrets["SAMBANOVA_API_KEY"]
)

@tool('search_tool')
def search_tool(query: str):
    """Deep forensic search."""
    search = DuckDuckGoSearchRun()
    return search.run(query)[:500]

# # 4. Sidebar Dashboard
with st.sidebar:
    st.markdown('<p style="color:#38bdf8; font-weight:900; font-size:1.6rem;">🛡️ Satyarth Control</p>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown('<div class="metric-container"><b>SambaNova Engine</b><br><small>STATUS: ACTIVE 🟢</small></div>', unsafe_allow_html=True)
    st.markdown('<div class="metric-container"><b>Forensic Agents</b><br><small>MODE: HYPER-LOCAL 📍</small></div>', unsafe_allow_html=True)
    st.markdown('<div class="metric-container"><b>Memory Buffer</b><br><small>USAGE: OPTIMAL 100% ✅</small></div>', unsafe_allow_html=True)
    
    with st.expander("ℹ️ How Satyarth-AI Works?"):
        st.markdown("""
        - **Scout Agent:** Gov portals aur regional news sources ko scan karta hai.
        - **Analyst Agent:** Evidence collect karke Hinglish report likhta hai.
        - **Image Forensic:** Pixels analyze karke AI markers dhundta hai.
        """)

    st.write("---")
    st.markdown('<p class="dev-label">Developed by Team Future Flux</p>', unsafe_allow_html=True)
    st.markdown('<p class="email-text">📩 satyarthai2007@gmail.com</p>', unsafe_allow_html=True)
    st.markdown('<p style="color:#94a3b8; font-weight:700; margin-top:10px;">📍 NIT Hamirpur</p>', unsafe_allow_html=True)

# # 5. Main Dashboard
st.markdown('<div class="scanner"></div>', unsafe_allow_html=True) 
st.markdown('<h1 class="main-title">SATYARTH-AI</h1>', unsafe_allow_html=True)
st.write("---")

tab1, tab2 = st.tabs(["🔍 Text Verification", "🔬 Image Investigation"])

# --- TAB 1 ---
with tab1:
    col_in, col_loc = st.columns([2, 1])
    with col_in:
        news_topic = st.text_input("News Headline Daalein 👇", placeholder="e.g. Is NIT Hamirpur technical fest postponed?")
    with col_loc:
        region = st.text_input("Region (Optional) 📍", placeholder="e.g. Hamirpur, Himachal Pradesh")

    st.markdown('<div class="text-btn-container">', unsafe_allow_html=True)
    if st.button("🚀 START DEEP FORENSIC ANALYSIS", key="text_btn"):
        if news_topic:
            with st.status("🕵️ Investigating live sources...", expanded=True) as status:
                scout = Agent(role='Scout', goal=f'Verify {news_topic} in {region}.', backstory="Detective.", tools=[search_tool], llm=text_llm)
                analyst = Agent(role='Verifier', goal='Write Hinglish report.', backstory="Lead Analyst.", llm=text_llm)
                crew = Crew(agents=[scout, analyst], tasks=[Task(description=f"Check {news_topic}", agent=scout, expected_output="Facts"), Task(description="Report", agent=analyst, expected_output="Report")], process=Process.sequential)
                result = crew.kickoff()
                st.session_state.final_report = result.raw
                status.update(label="Analysis Complete! ✅", state="complete")
            st.balloons()
    st.markdown('</div>', unsafe_allow_html=True)

    if "final_report" in st.session_state:
        st.markdown(f'<div style="background:rgba(255,255,255,0.1); border:2px solid #38bdf8; padding:35px; border-radius:20px; line-height:1.8;"><h3>📜 Forensic Verification Report</h3>{st.session_state.final_report}</div>', unsafe_allow_html=True)
        st.write("---")
        st.markdown('<div class="colorful-btn">', unsafe_allow_html=True)
        if st.button("👥 Request Human Verification"):
            st.info("you will be informed when we receive reply")
        st.markdown('</div>', unsafe_allow_html=True)

# --- TAB 2 ---
with tab2:
    st.markdown("### 🔬 Image Forensic Module")
    cam_on = st.toggle("🎥 Activate Live Camera Feed", value=False)
    up_c, cam_c = st.columns(2)
    img_cam = None 
    with up_c: img_up = st.file_uploader("Upload Image", type=['jpg','png','jpeg'])
    with cam_c: 
        if cam_on: img_cam = st.camera_input("Take Photo")
        else: st.info("Camera is OFF.")

    # ERROR FIX: Explicit None-Check to avoid TypeError on line 154
    final_img = img_up if img_up is not None else img_cam
    
    if final_img is not None:
        st.image(final_img, caption="Forensic Scan Ready.", width=500)
        if st.button("🔍 RUN PIXEL ANALYSIS", key="img_btn"):
            with st.spinner("Analyzing pixels..."):
                try:
                    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    response = model.generate_content(["Analyze image for AI artifacts. Hinglish Verdict.", Image.open(final_img)])
                    st.write(f"### 🔬 Verdict: \n {response.text}")
                except Exception as e: st.error(f"Error: {e}")
