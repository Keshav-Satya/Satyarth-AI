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

# # 2. Force Visibility & High-Contrast Cyber CSS
st.markdown("""
    <style>
    /* Global Background */
    .stApp { background: #020617; color: #ffffff; }
    
    /* Neon Sidebar - Extreme Contrast Fix */
    [data-testid="stSidebar"] {
        background-color: #020617 !important;
        border-right: 3px solid #0ea5e9;
    }
    .metric-container {
        background: rgba(14, 165, 233, 0.3);
        padding: 18px; border-radius: 12px;
        border: 2px solid #38bdf8; margin-bottom: 18px;
    }
    .metric-container b { color: #ffffff !important; font-size: 1.25rem; }
    .metric-container small { color: #38bdf8 !important; font-weight: 900; letter-spacing: 1px; }
    
    /* Expander Text Readability (How it works) */
    .stExpander { border: 1px solid #38bdf8 !important; background: rgba(255, 255, 255, 0.05) !important; }
    .stExpander p, .stExpander li { color: #ffffff !important; font-weight: 700; font-size: 1rem; }

    /* Decorated Title with Multi-Glow */
    .main-title {
        background: linear-gradient(90deg, #38bdf8, #ffffff, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 5rem; font-weight: 900; text-align: center;
        filter: drop-shadow(0 0 20px rgba(56, 189, 248, 0.8));
    }

    /* Live Scanning Bar Animation */
    .scanner {
        width: 100%; height: 5px; background: #38bdf8;
        box-shadow: 0 0 15px #38bdf8; position: relative; overflow: hidden;
        margin-bottom: 20px; border-radius: 5px;
    }
    .scanner::after {
        content: ''; display: block; width: 200px; height: 100%;
        background: #ffffff; box-shadow: 0 0 30px #ffffff;
        position: absolute; animation: scan 2s linear infinite;
    }
    @keyframes scan { 0% { left: -200px; } 100% { left: 100%; } }

    /* GREEN Labels for Headlines & Region - High Visibility */
    [data-testid="stWidgetLabel"] p {
        font-size: 1.4rem !important; 
        font-weight: 900 !important; 
        color: #ffffff !important; /* White text on green bg for contrast */
        background: #16a34a !important; /* Solid Green */
        padding: 8px 20px; 
        border-radius: 8px;
        display: inline-block; 
        margin-bottom: 15px !important; 
        border-bottom: 4px solid #14532d;
    }

    /* BUTTON VISIBILITY FIX - NO MORE WHITE-ON-WHITE */
    .stButton>button {
        color: #ffffff !important; /* Text ALWAYS White */
        font-weight: 900 !important;
        font-size: 1.2rem !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        border-radius: 12px !important;
        padding: 15px 30px !important;
        border: 2px solid #ffffff !important;
        transition: 0.3s;
    }

    /* Start Analysis Button (Deep Blue) */
    .main-btn .stButton>button {
        background: linear-gradient(45deg, #2563eb, #1d4ed8) !important;
    }

    /* Request Human Verification (Vibrant Red-Orange) */
    .human-btn .stButton>button {
        background: linear-gradient(45deg, #dc2626, #ea580c) !important;
    }

    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 30px rgba(255, 255, 255, 0.3);
    }
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
    """Forensic web scan tool."""
    search = DuckDuckGoSearchRun()
    return search.run(query)[:500]

# # 4. Sidebar Dashboard
with st.sidebar:
    st.markdown('<p style="color:#38bdf8; font-weight:900; font-size:1.8rem;">🛡️ Satyarth Control</p>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown('<div class="metric-container"><b>SambaNova Engine</b><br><small>STATUS: ACTIVE 🟢</small></div>', unsafe_allow_html=True)
    st.markdown('<div class="metric-container"><b>Forensic Agents</b><br><small>MODE: HYPER-LOCAL 📍</small></div>', unsafe_allow_html=True)
    st.markdown('<div class="metric-container"><b>Memory Buffer</b><br><small>USAGE: OPTIMAL 100% ✅</small></div>', unsafe_allow_html=True)
    
    with st.expander("ℹ️ How Satyarth-AI Works?"):
        st.markdown("""
        - **Scout Agent:** Gov portals aur news sites scan karta hai.
        - **Analyst Agent:** Hinglish forensic report likhta hai.
        - **Vision AI:** Pixels analyze karke AI markers dhundta hai.
        """)

    st.write("---")
    st.markdown('<p style="color:#38bdf8; font-weight:900; font-size:1.1rem;">Developed by Team Future Flux</p>', unsafe_allow_html=True)
    st.markdown('<p style="color:#ffffff; font-weight:800; background:#0ea5e9; padding:5px 10px; border-radius:5px;">📩 satyarthai2007@gmail.com</p>', unsafe_allow_html=True)
    st.markdown('<p style="color:#94a3b8; font-weight:700; margin-top:10px;">📍 NIT Hamirpur</p>', unsafe_allow_html=True)

# # 5. Main UI Header
st.markdown('<div class="scanner"></div>', unsafe_allow_html=True) 
st.markdown('<h1 class="main-title">SATYARTH-AI</h1>', unsafe_allow_html=True)
st.write("---")

tab1, tab2 = st.tabs(["🔍 Text Verification", "🔬 Image Investigation"])

with tab1:
    col_in, col_loc = st.columns([2, 1])
    with col_in:
        news_topic = st.text_input("News Headline Daalein 👇", placeholder="e.g. Is viral news authentic?")
    with col_loc:
        region = st.text_input("Region (Optional) 📍", placeholder="District, State")

    st.markdown('<div class="main-btn">', unsafe_allow_html=True)
    if st.button("🚀 START DEEP FORENSIC ANALYSIS", key="text_btn"):
        if news_topic:
            with st.status("🕵️ Investigating sources...", expanded=True) as status:
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
        st.markdown('<div class="human-btn">', unsafe_allow_html=True)
        if st.button("👥 Request Human Verification"):
            st.info("you will be informed when we receive reply")
        st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown("### 🔬 Image Forensic Module")
    cam_on = st.toggle("🎥 Activate Live Camera Feed", value=False)
    up_c, cam_c = st.columns(2)
    img_cam = None 
    with up_c: img_up = st.file_uploader("Upload Image", type=['jpg','png','jpeg'])
    with cam_c: 
        if cam_on: img_cam = st.camera_input("Take Photo")
        else: st.info("Camera is OFF.")

    final_img = img_up if img_up is not None else img_cam
    if final_img is not None:
        st.image(final_img, caption="Forensic Scan Ready.", width=500)
        st.markdown('<div class="main-btn">', unsafe_allow_html=True)
        if st.button("🔍 RUN PIXEL ANALYSIS", key="img_btn"):
            with st.spinner("Scanning for AI markers..."):
                try:
                    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    response = model.generate_content(["Analyze image for AI artifacts. Hinglish Verdict.", Image.open(final_img)])
                    st.write(f"### 🔬 Verdict: \n {response.text}")
                except Exception as e: st.error(f"Error: {e}")
        st.markdown('</div>', unsafe_allow_html=True)
