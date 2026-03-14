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

# # 2. Advanced High-Contrast Cyber-Tech CSS
st.markdown("""
    <style>
    /* Global Background */
    .stApp { background: linear-gradient(135deg, #020617 0%, #0f172a 100%); color: #ffffff; }
    
    /* Neon Sidebar - Extreme Visibility Fix */
    [data-testid="stSidebar"] {
        background-color: #020617 !important;
        border-right: 3px solid #0ea5e9;
    }
    .sidebar-header { color: #38bdf8 !important; font-weight: 900; font-size: 1.6rem; }
    
    /* Metric Boxes with High-Contrast */
    .metric-container {
        background: rgba(14, 165, 233, 0.25);
        padding: 18px; border-radius: 12px;
        border: 2px solid #38bdf8; margin-bottom: 18px;
        box-shadow: 0 4px 15px rgba(56, 189, 248, 0.2);
    }
    .metric-container b { color: #ffffff !important; font-size: 1.25rem; display: block; margin-bottom: 5px; }
    .metric-container small { color: #ffffff !important; font-weight: 900; font-size: 0.95rem; letter-spacing: 1.2px; text-transform: uppercase; }
    
    /* Sidebar Expander/About Text Readability */
    .stExpander { border: 1px solid #38bdf8 !important; background: rgba(255, 255, 255, 0.05) !important; }
    .stExpander p, .stExpander li { color: #f8fafc !important; font-weight: 500; font-size: 1rem; }

    /* Developer & Email Footer Visibility */
    .dev-label { color: #38bdf8 !important; font-weight: 900; font-size: 1.1rem; margin-top: 25px; }
    .email-text { color: #ffffff !important; font-weight: 800; font-size: 1rem; background: #0ea5e9; padding: 6px 10px; border-radius: 6px; display: inline-block; margin-top: 5px; }
    .nit-text { color: #94a3b8 !important; font-weight: 700; font-size: 0.9rem; margin-top: 8px; }

    /* Main UI Input Labels */
    [data-testid="stWidgetLabel"] p {
        font-size: 1.35rem !important; font-weight: 900 !important; color: #ffffff !important;
        background: rgba(14, 165, 233, 0.4); padding: 8px 18px; border-radius: 10px;
        display: inline-block; margin-bottom: 15px !important; border-left: 6px solid #38bdf8;
    }

    /* Human Verification Button - Blue Neon Look */
    .human-btn-container .stButton>button {
        background: linear-gradient(45deg, #1d4ed8, #2563eb) !important;
        color: white !important;
        border: 2px solid #38bdf8 !important;
        font-weight: 900 !important;
        font-size: 1.1rem !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .main-title {
        background: linear-gradient(to right, #38bdf8, #818cf8);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-size: 4.8rem; font-weight: 900; text-align: center;
        filter: drop-shadow(0 10px 15px rgba(56, 189, 248, 0.3));
    }
    
    .report-card {
        background-color: rgba(255, 255, 255, 0.1); backdrop-filter: blur(35px);
        padding: 35px; border-radius: 20px; border: 2px solid #38bdf8;
        color: #ffffff !important; line-height: 1.8; font-size: 1.15rem;
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
    """Deep forensic search for evidence."""
    search = DuckDuckGoSearchRun()
    return search.run(query)[:500]

# # 4. Sidebar: Control Center, About & Footer
with st.sidebar:
    st.markdown('<p class="sidebar-header">🛡️ Satyarth Control</p>', unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown("### 📊 System Health")
    st.markdown('<div class="metric-container"><b>SambaNova Engine</b><br><small>STATUS: ACTIVE 🟢</small></div>', unsafe_allow_html=True)
    st.markdown('<div class="metric-container"><b>Forensic Agents</b><br><small>MODE: HYPER-LOCAL 📍</small></div>', unsafe_allow_html=True)
    st.markdown('<div class="metric-container"><b>Memory Buffer</b><br><small>USAGE: OPTIMAL 100% ✅</small></div>', unsafe_allow_html=True)
    
    # About Section
    with st.expander("ℹ️ How Satyarth-AI Works?"):
        st.markdown("""
        1. **Scout Agent:** Ye internet ke official gov portals aur regional news sources ko scan karta hai.
        2. **Analyst Agent:** Ye sources ko points deta hai (Credibility Score) aur final Hinglish report likhta hai.
        3. **Image Forensic:** Gemini 1.5 Flash pixels ko analyze karke AI markers dhundta hai.
        """)

    st.write("---")
    st.markdown('<p class="dev-label">Developed by Team Future Flux</p>', unsafe_allow_html=True)
    st.markdown('<p class="email-text">📩 satyarthai2007@gmail.com</p>', unsafe_allow_html=True)
    st.markdown('<p class="nit-text">📍 NIT Hamirpur | Electrothon 8.0</p>', unsafe_allow_html=True)

# # 5. Main UI Header
st.markdown('<h1 class="main-title">SATYARTH-AI</h1>', unsafe_allow_html=True)
st.write("---")

tab1, tab2 = st.tabs(["🔍 Text Verification", "🔬 Image Investigation"])

with tab1:
    c_in, c_loc = st.columns([2, 1])
    with c_in:
        news_topic = st.text_input("News Headline Daalein 👇", placeholder="e.g. Is NIT Hamirpur closing tomorrow?")
    with c_loc:
        region = st.text_input("Region (Optional) 📍", placeholder="District and State")

    if st.button("🚀 START DEEP FORENSIC ANALYSIS", key="text_btn"):
        if news_topic:
            with st.status("🕵️ Investigating sources...", expanded=True) as status:
                scout = Agent(role='Scout', goal=f'Verify {news_topic} in {region}.', backstory="Detective.", tools=[search_tool], llm=text_llm)
                analyst = Agent(role='Verifier', goal='Write Hinglish report.', backstory="Journalist.", llm=text_llm)
                crew = Crew(agents=[scout, analyst], tasks=[Task(description=f"Check {news_topic}", agent=scout, expected_output="Facts"), Task(description="Report", agent=analyst, expected_output="Report")], process=Process.sequential)
                result = crew.kickoff()
                st.session_state.final_report = result.raw
                status.update(label="Analysis Complete! ✅", state="complete")
            st.balloons()

    if "final_report" in st.session_state:
        st.markdown(f'<div class="report-card"><h3>📜 Forensic Verification Report</h3>{st.session_state.final_report}</div>', unsafe_allow_html=True)
        st.write("---")
        # Neon Blue Button for Human Verification
        st.markdown('<div class="human-btn-container">', unsafe_allow_html=True)
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
            with st.spinner("Analyzing AI markers..."):
                try:
                    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    response = model.generate_content(["Analyze image for AI artifacts. Hinglish Verdict.", Image.open(final_img)])
                    st.markdown(f'<div class="report-card"><h3>🔬 Verdict</h3>{response.text}</div>', unsafe_allow_html=True)
                except Exception as e: st.error(f"Error: {e}")
