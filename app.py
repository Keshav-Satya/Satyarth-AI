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

# # 2. Advanced High-Contrast Cyber CSS
st.markdown("""
    <style>
    /* Global Background */
    .stApp { background: #020617 !important; color: #ffffff !important; }
    
    /* Decorated Title with Neon Glow */
    .main-title {
        color: #38bdf8 !important;
        font-size: 4.5rem;
        font-weight: 900;
        text-align: center;
        text-shadow: 0 0 20px rgba(56, 189, 248, 0.8);
        margin-bottom: 10px;
    }

    /* Live Scanning Bar Animation */
    .scanner {
        width: 100%; height: 6px; background: #38bdf8;
        box-shadow: 0 0 20px #38bdf8; position: relative; overflow: hidden;
        margin-bottom: 25px; border-radius: 10px;
    }
    .scanner::after {
        content: ''; display: block; width: 250px; height: 100%;
        background: #ffffff; position: absolute; animation: scan 2s linear infinite;
    }
    @keyframes scan { 0% { left: -250px; } 100% { left: 100%; } }

    /* 🔴 SIMPLE RED TABS (Requested Change) */
    button[data-baseweb="tab"] {
        background-color: transparent !important;
        color: #94a3b8 !important;
        font-weight: 700 !important;
        border: none !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        border-bottom: 4px solid #ef4444 !important; /* Simple Red Line */
        color: #ffffff !important;
    }

    /* 💚 GREEN LABELS for Headline & Region */
    [data-testid="stWidgetLabel"] p {
        font-size: 1.35rem !important; 
        font-weight: 900 !important; 
        color: #ffffff !important; 
        background: #16a34a !important; /* Solid Green */
        padding: 8px 20px !important; 
        border-radius: 8px !important;
        display: inline-block !important; 
        border: 2px solid #ffffff !important;
    }

    /* Blue Input Boxes Fix */
    div[data-baseweb="input"] {
        background-color: #0f172a !important;
        border: 2px solid #38bdf8 !important;
    }
    input { color: #ffffff !important; font-weight: 700 !important; }

    /* BUTTONS STYLE */
    .stButton>button {
        color: #ffffff !important;
        font-weight: 900 !important;
        font-size: 1.1rem !important;
        text-transform: uppercase;
        border-radius: 12px !important;
        padding: 15px 30px !important;
        border: 2px solid #ffffff !important;
        transition: 0.3s;
    }

    /* Deep Blue Analysis Button */
    .main-btn .stButton>button {
        background: #1e40af !important;
    }

    /* 🔴 RED Human Verification Button */
    .red-btn .stButton>button {
        background: #dc2626 !important;
    }

    /* Sidebar Health Metrics */
    [data-testid="stSidebar"] { background-color: #020617 !important; border-right: 3px solid #38bdf8; }
    .metric-container {
        background: #1e293b !important; padding: 15px; border-radius: 12px;
        border: 2px solid #38bdf8; margin-bottom: 15px;
    }
    .metric-container b, .metric-container small { color: #ffffff !important; }

    /* Expander/About Visibility */
    .stExpander { border: 2px solid #38bdf8 !important; background: #0f172a !important; }
    .stExpander p, .stExpander li { color: #ffffff !important; font-weight: 700; }

    /* Report Card Styling */
    .report-card {
        background-color: rgba(255, 255, 255, 0.1); backdrop-filter: blur(25px);
        padding: 30px; border-radius: 20px; border: 2px solid #38bdf8;
        color: #ffffff !important; line-height: 1.8;
    }
    </style>
    """, unsafe_allow_html=True)

# # 3. Engine Setup
if "SAMBANOVA_API_KEY" not in st.secrets:
    st.error("Sir, Secrets mein SAMBANOVA_API_KEY missing hai!")
    st.stop()

text_llm = LLM(
    model="sambanova/Meta-Llama-3.3-70B-Instruct", 
    base_url="https://api.sambanova.ai/v1",
    api_key=st.secrets["SAMBANOVA_API_KEY"]
)

@tool('search_tool')
def search_tool(query: str):
    """Forensic search for news evidence."""
    search = DuckDuckGoSearchRun()
    return search.run(query)[:500]

# # 4. Sidebar: Dashboard & About
with st.sidebar:
    st.markdown('<p style="color:#38bdf8; font-weight:900; font-size:1.8rem;">🛡️ Satyarth Control</p>', unsafe_allow_html=True)
    st.write("---")
    st.markdown('<div class="metric-container"><b>SambaNova Engine</b><br><small>STATUS: ACTIVE 🟢</small></div>', unsafe_allow_html=True)
    st.markdown('<div class="metric-container"><b>Forensic Agents</b><br><small>MODE: HYPER-LOCAL 📍</small></div>', unsafe_allow_html=True)
    
    with st.expander("ℹ️ How Satyarth-AI Works?"):
        st.write("- **Scout Agent:** Gov portals aur regional sources scan karta hai.")
        st.write("- **Analyst Agent:** Hinglish forensic report likhta hai.")
        st.write("- **Vision AI:** Pixels analyze karke AI markers dhundta hai.")

    st.write("---")
    st.markdown('<p style="color:#38bdf8; font-weight:900;">Developed by Team Future Flux</p>', unsafe_allow_html=True)
    st.markdown('<p style="color:#ffffff; font-weight:800; background:#2563eb; padding:5px 12px; border-radius:6px; border:1px solid white;">📩 satyarthai2007@gmail.com</p>', unsafe_allow_html=True)
    st.markdown('<p style="color:#ffffff; font-weight:800; margin-top:10px;">📍 NIT Hamirpur</p>', unsafe_allow_html=True)

# # 5. Main UI Header
st.markdown('<div class="scanner"></div>', unsafe_allow_html=True) 
st.markdown('<h1 class="main-title">🕵️ SATYARTH-AI 🕵️</h1>', unsafe_allow_html=True)
st.write("---")

tab1, tab2 = st.tabs(["📝 Text Verification", "🔬 Image Investigation"])

# --- TAB 1: TEXT ---
with tab1:
    col_in, col_loc = st.columns([2, 1])
    with col_in:
        news_topic = st.text_input("News Headline Daalein 👇", placeholder="e.g. Is viral news authentic?")
    with col_loc:
        region = st.text_input("Region (Optional) 📍", placeholder="District and State")

    st.markdown('<div class="main-btn">', unsafe_allow_html=True)
    if st.button("🚀 START DEEP FORENSIC ANALYSIS", key="text_btn"):
        if news_topic:
            with st.status("🕵️ Investigating live sources...", expanded=True) as status:
                scout = Agent(role='Scout', goal=f'Verify {news_topic} in {region}.', backstory="Detective.", tools=[search_tool], llm=text_llm)
                analyst = Agent(role='Verifier', goal='Write professional Hinglish report.', backstory="Lead Analyst.", llm=text_llm)
                crew = Crew(agents=[scout, analyst], tasks=[Task(description=f"Check {news_topic}", agent=scout, expected_output="Facts"), Task(description="Report", agent=analyst, expected_output="Report")], process=Process.sequential)
                result = crew.kickoff()
                st.session_state.final_report = result.raw
                status.update(label="Analysis Complete! ✅", state="complete")
            st.balloons()
    st.markdown('</div>', unsafe_allow_html=True)

    if "final_report" in st.session_state:
        st.markdown(f'<div class="report-card"><h3>📜 Forensic Verification Report</h3>{st.session_state.final_report}</div>', unsafe_allow_html=True)
        st.write("---")
        st.markdown('<div class="red-btn">', unsafe_allow_html=True)
        if st.button("👥 Request Human Verification"):
            st.info("you will be informed when we receive reply")
        st.markdown('</div>', unsafe_allow_html=True)

# --- TAB 2: IMAGE ---
with tab2:
    st.markdown("### 🔬 Image Forensic Module")
    cam_on = st.toggle("🎥 Activate Live Camera Feed", value=False)
    up_c, cam_c = st.columns(2)
    img_cam = None 
    with up_c: img_up = st.file_uploader("Upload Image", type=['jpg','png','jpeg'])
    with cam_c: 
        if cam_on: img_cam = st.camera_input("Take Photo")
        else: st.info("Camera is OFF.")

    # Fix logic for Line 154 error
    final_img = img_up if img_up is not None else img_cam
    
    if final_img is not None:
        st.image(final_img, caption="Forensic Scan Ready.", width=500)
        if st.button("🔍 RUN PIXEL ANALYSIS", key="img_btn"):
            with st.spinner("Scanning for AI markers..."):
                try:
                    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    response = model.generate_content(["Analyze image for AI markers. Hinglish Verdict.", Image.open(final_img)])
                    st.write(f"### 🔬 Verdict: \n {response.text}")
                except Exception as e: st.error(f"Error: {e}")
