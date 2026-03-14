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

# # 2. NUCLEAR CSS - Unbreakable Readability Overwrite
st.markdown("""
    <style>
    /* Global - Force Deep Dark Theme */
    .stApp { background: #020617 !important; color: #ffffff !important; }
    
    /* INPUT BOXES - Blue Dibbe Fix */
    div[data-baseweb="input"], div[data-baseweb="base-input"] {
        background-color: #0f172a !important; 
        border: 2px solid #38bdf8 !important; 
        border-radius: 10px !important;
    }
    input, textarea {
        color: #ffffff !important; 
        -webkit-text-fill-color: #ffffff !important;
        font-weight: 700 !important;
    }

    /* GREEN LABELS - News & Region */
    [data-testid="stWidgetLabel"] p {
        font-size: 1.4rem !important; 
        font-weight: 900 !important; 
        color: #ffffff !important; 
        background: #16a34a !important; 
        padding: 8px 20px !important; 
        border-radius: 8px !important;
        display: inline-block !important; 
        border: 2px solid #ffffff !important;
    }

    /* THE ULTIMATE BUTTON FIX - No more white rectangles! */
    button, .stButton>button {
        background-color: #1e40af !important; /* Deep Blue Requested */
        color: #ffffff !important; /* Bold White Text */
        -webkit-text-fill-color: #ffffff !important;
        font-weight: 900 !important;
        font-size: 1.2rem !important;
        text-transform: uppercase !important;
        border: 3px solid #ffffff !important;
        border-radius: 12px !important;
        padding: 15px 30px !important;
        opacity: 1 !important;
        visibility: visible !important;
        display: block !important;
        box-shadow: 0 4px 15px rgba(56, 189, 248, 0.4) !important;
    }

    /* Specific Red Button for Human Verification */
    .red-btn button, .red-btn .stButton>button {
        background: #dc2626 !important; /* Solid Red */
        border: 3px solid #ffffff !important;
    }

    button:hover { 
        transform: scale(1.03) !important; 
        filter: brightness(1.2) !important; 
    }

    /* Sidebar Readability Fix */
    [data-testid="stSidebar"] {
        background-color: #020617 !important;
        border-right: 3px solid #38bdf8 !important;
    }
    .metric-container {
        background: #1e293b !important;
        padding: 18px; border-radius: 12px;
        border: 2px solid #38bdf8; margin-bottom: 18px;
    }
    .metric-container b, .metric-container small { color: #ffffff !important; }

    /* About Expander Visibility Fix */
    .stExpander { border: 2px solid #38bdf8 !important; background: #0f172a !important; }
    .stExpander p, .stExpander li, .stExpander span { 
        color: #ffffff !important; 
        font-weight: 800 !important;
        -webkit-text-fill-color: #ffffff !important;
    }

    /* Title & Scanner */
    .main-title {
        color: #38bdf8 !important;
        font-size: 5rem; font-weight: 900; text-align: center;
        text-shadow: 0 0 20px #38bdf8;
    }
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

    /* Footer Info */
    .email-box { color: #ffffff !important; font-weight: 800; background: #2563eb; padding: 5px 15px; border-radius: 6px; border: 2px solid white; display: inline-block; }
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
    st.write("---")
    st.markdown('<div class="metric-container"><b>SambaNova Engine</b><br><small>STATUS: ACTIVE 🟢</small></div>', unsafe_allow_html=True)
    st.markdown('<div class="metric-container"><b>Forensic Agents</b><br><small>MODE: HYPER-LOCAL 📍</small></div>', unsafe_allow_html=True)
    st.markdown('<div class="metric-container"><b>Memory Buffer</b><br><small>USAGE: OPTIMAL 100% ✅</small></div>', unsafe_allow_html=True)
    
    with st.expander("ℹ️ How Satyarth-AI Works?"):
        st.write("- **Scout Agent:** Gov portals scan karta hai.")
        st.write("- **Analyst Agent:** Hinglish report likhta hai.")
        st.write("- **Vision AI:** Pixels analyze karta hai.")

    st.write("---")
    st.markdown('<p style="color:#38bdf8; font-weight:900;">Developed by Team Future Flux</p>', unsafe_allow_html=True)
    st.markdown('<p class="email-box">📩 satyarthai2007@gmail.com</p>', unsafe_allow_html=True)
    st.markdown('<p style="color:#ffffff; font-weight:800; margin-top:10px;">📍 NIT Hamirpur</p>', unsafe_allow_html=True)

# # 5. Main UI Header
st.markdown('<div class="scanner"></div>', unsafe_allow_html=True) 
st.markdown('<h1 class="main-title">SATYARTH-AI</h1>', unsafe_allow_html=True)
st.write("---")

tab1, tab2 = st.tabs(["🔍 Text Verification", "🔬 Image Investigation"])

with tab1:
    col_in, col_loc = st.columns([2, 1])
    with col_in:
        news_topic = st.text_input("News Headline Daalein 👇", placeholder="e.g. Enter viral news headline...")
    with col_loc:
        region = st.text_input("Region (Optional) 📍", placeholder="e.g. Hamirpur, Himachal")

    # Force Visibility Container for Button
    st.markdown('<div class="main-btn-container">', unsafe_allow_html=True)
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
        st.markdown(f'<div style="background:rgba(255,255,255,0.1); border:3px solid #38bdf8; padding:35px; border-radius:20px; line-height:1.8;"><h3>📜 Forensic Verification Report</h3>{st.session_state.final_report}</div>', unsafe_allow_html=True)
        st.write("---")
        st.markdown('<div class="red-btn">', unsafe_allow_html=True)
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
        if st.button("🔍 RUN PIXEL ANALYSIS", key="img_btn"):
            with st.spinner("Analyzing pixels..."):
                try:
                    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    response = model.generate_content(["Analyze image for AI markers. Hinglish Verdict.", Image.open(final_img)])
                    st.write(f"### 🔬 Verdict: \n {response.text}")
                except Exception as e: st.error(f"Error: {e}")
