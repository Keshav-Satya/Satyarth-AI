import streamlit as st
import os
import base64
from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun
from PIL import Image
import google.generativeai as genai

# # 1. Page Configuration
st.set_page_config(page_title="Satyarth-AI | Forensic Engine", page_icon="🕵️", layout="wide")

# # 2. NUCLEAR CSS - High Contrast & Visibility Logic
st.markdown("""
    <style>
    /* Global Background */
    .stApp { background: #020617 !important; color: #ffffff !important; }

    /* Decorated Title with Emojis */
    .main-title {
        color: #38bdf8 !important;
        font-size: 4.5rem; font-weight: 900; text-align: center;
        text-shadow: 0 0 20px rgba(56, 189, 248, 0.8);
        margin-bottom: 20px;
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

    /* 🔴 SIMPLE RED TABS */
    button[data-baseweb="tab"] {
        background-color: transparent !important; color: #94a3b8 !important;
        font-weight: 700 !important; border: none !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        border-bottom: 4px solid #ef4444 !important; color: #ffffff !important;
    }

    /* 💚 GREEN LABELS for Headline & Region */
    [data-testid="stWidgetLabel"] p {
        font-size: 1.35rem !important; font-weight: 900 !important; color: #ffffff !important; 
        background: #16a34a !important; padding: 8px 20px !important; 
        border-radius: 8px !important; display: inline-block !important; 
        border: 2px solid #ffffff !important;
    }

    /* 🔵 TYPED TEXT COLOUR: BLUE */
    div[data-baseweb="input"] { background-color: #0f172a !important; border: 2px solid #38bdf8 !important; }
    input, textarea {
        color: #38bdf8 !important; font-weight: 800 !important;
        -webkit-text-fill-color: #38bdf8 !important;
    }

    /* BUTTONS STYLE */
    .stButton>button {
        font-weight: 900 !important; font-size: 1.2rem !important;
        text-transform: uppercase; border-radius: 12px !important;
        padding: 15px 30px !important; border: 3px solid #ffffff !important;
        transition: 0.3s;
    }

    /* ⬇️ START Analysis Button (Deep Blue Bg + RED TEXT) ⬇️ */
    .main-btn .stButton>button {
        background: #1e40af !important;
        color: #ef4444 !important; /* Force RED Text requested */
        -webkit-text-fill-color: #ef4444 !important;
    }

    /* 🔴 RED Human Verification Button */
    .red-btn .stButton>button {
        background: #dc2626 !important;
        color: #ffffff !important; -webkit-text-fill-color: #ffffff !important;
    }

    /* Sidebar & Expander Readability */
    [data-testid="stSidebar"] { background-color: #020617 !important; border-right: 3px solid #38bdf8; }
    .metric-container { background: #1e293b !important; padding: 15px; border-radius: 12px; border: 2px solid #38bdf8; margin-bottom: 15px; }
    .stExpander { border: 2px solid #38bdf8 !important; background: #0f172a !important; }
    .stExpander p, .stExpander li { color: #ffffff !important; font-weight: 700; }

    /* Report Card */
    .report-card { background-color: rgba(255, 255, 255, 0.1); backdrop-filter: blur(25px); padding: 30px; border-radius: 20px; border: 2px solid #38bdf8; color: #ffffff !important; line-height: 1.8; }
    </style>
    """, unsafe_allow_html=True)

# # 3. Engine Setup
if "SAMBANOVA_API_KEY" not in st.secrets:
    st.error("Sir, Secrets mein SAMBANOVA_API_KEY check karein!")
    st.stop()

text_llm = LLM(
    model="sambanova/Meta-Llama-3.3-70B-Instruct", 
    base_url="https://api.sambanova.ai/v1",
    api_key=st.secrets["SAMBANOVA_API_KEY"]
)

@tool('search_tool')
def search_tool(query: str):
    """Deep forensic search for news evidence."""
    search = DuckDuckGoSearchRun()
    return search.run(query)[:500]

# # 4. Sidebar Dashboard
with st.sidebar:
    st.markdown('<p style="color:#38bdf8; font-weight:900; font-size:1.8rem;">🕵️ Satyarth AI</p>', unsafe_allow_html=True)
    st.write("---")
    st.markdown('<div class="metric-container"><b>SambaNova Engine</b><br><small>STATUS: ACTIVE 🟢</small></div>', unsafe_allow_html=True)
    st.markdown('<div class="metric-container"><b>Forensic Agents</b><br><small>MODE: HYPER-LOCAL 📍</small></div>', unsafe_allow_html=True)
    
    with st.expander("ℹ️ How Satyarth-AI Works?"):
        st.write("- **Scout Agent:** Gov portals scan karta hai.")
        st.write("- **Analyst Agent:** Hinglish report likhta hai.")
        st.write("- **Vision AI:** Pixels analyze karta hai.")

    st.write("---")
    st.markdown('<p style="color:#38bdf8; font-weight:900;">Developed by Team Future Flux</p>', unsafe_allow_html=True)
    st.markdown('<p style="color:#ffffff; font-weight:800; background:#2563eb; padding:5px 12px; border-radius:6px; border:1px solid white;">📩 satyarthai2007@gmail.com</p>', unsafe_allow_html=True)
    st.markdown('<p style="color:#ffffff; font-weight:800; margin-top:10px;">📍 NIT Hamirpur</p>', unsafe_allow_html=True)

# # 5. Header
st.markdown('<div class="scanner"></div>', unsafe_allow_html=True) 
st.markdown('<h1 class="main-title">🕵️ SATYARTH-AI 🕵️</h1>', unsafe_allow_html=True)
st.write("---")

tab1, tab2 = st.tabs(["📝 Text Verification", "🔬 Image Investigation"])

# --- TAB 1: TEXT ---
with tab1:
    col1, col2 = st.columns([2, 1])
    with col1:
        news_topic = st.text_input("News Headline Daalein 👇", placeholder="e.g. Enter news headline...")
    with col2:
        region = st.text_input("Region (Optional) 📍", placeholder="District, State")

    st.markdown('<div class="main-btn">', unsafe_allow_html=True)
    if st.button("🚀 START DEEP FORENSIC ANALYSIS", key="text_btn"):
        if news_topic:
            with st.status("🕵️ Investigating live sources...", expanded=True) as status:
                scout = Agent(role='Scout', goal=f'Verify {news_topic} in {region}.', backstory="Detective.", tools=[search_tool], llm=text_llm)
                analyst = Agent(role='Verifier', goal='Write professional Hinglish report.', backstory="Lead Analyst.", llm=text_llm)
                
                # Fixed Indentation & Added max_rpm=1
                crew = Crew(
                    agents=[scout, analyst],
                    tasks=[
                        Task(description=f"Verify {news_topic}", agent=scout, expected_output="Facts"),
                        Task(description="Write Hinglish forensic report.", agent=analyst, expected_output="Report")
                    ],
                    process=Process.sequential,
                    max_rpm=1 # Sir, ye line rate limits se bachayegi
                )
                
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

    final_img = img_up if img_up is not None else img_cam
    if final_img is not None:
        st.image(final_img, caption="Forensic Scan Ready.", width=500)
        st.markdown('<div class="main-btn">', unsafe_allow_html=True)
        if st.button("🔍 RUN PIXEL ANALYSIS", key="img_btn"):
            with st.spinner("Analyzing AI markers..."):
                try:
                    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    response = model.generate_content(["Analyze image for AI artifacts. Hinglish Verdict.", Image.open(final_img)])
                    st.markdown(f'<div class="report-card"><h3>🔬 Verdict</h3>{response.text}</div>', unsafe_allow_html=True)
                except Exception as e: st.error(f"Error: {e}")
        st.markdown('</div>', unsafe_allow_html=True)
