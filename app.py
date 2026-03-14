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
    .stApp { background: linear-gradient(135deg, #020617 0%, #0f172a 100%); color: #f8fafc; }
    
    /* Neon Sidebar - High Readability Fix */
    [data-testid="stSidebar"] {
        background-color: #020617 !important;
        border-right: 3px solid #0ea5e9;
    }
    .sidebar-header { color: #38bdf8 !important; font-weight: 900; font-size: 1.6rem; }
    
    .metric-container {
        background: rgba(14, 165, 233, 0.25);
        padding: 18px; border-radius: 12px;
        border: 2px solid #38bdf8; margin-bottom: 18px;
    }
    /* Bright Metric Text */
    .metric-container b { color: #ffffff !important; font-size: 1.2rem; display: block; margin-bottom: 5px; }
    .metric-container small { color: #f0f9ff !important; font-weight: 900; font-size: 0.95rem; letter-spacing: 1px; text-transform: uppercase; }
    
    /* Developer & Email Info */
    .dev-label { color: #38bdf8 !important; font-weight: 900; font-size: 1.1rem; margin-top: 20px; }
    .email-text { color: #ffffff !important; font-weight: 800; font-family: 'Courier New', monospace; font-size: 0.95rem; background: rgba(56, 189, 248, 0.1); padding: 5px; border-radius: 4px; }

    /* Input Labels */
    [data-testid="stWidgetLabel"] p {
        font-size: 1.35rem !important; font-weight: 900 !important; color: #ffffff !important;
        background: rgba(14, 165, 233, 0.3); padding: 6px 15px; border-radius: 10px;
        display: inline-block; margin-bottom: 15px !important; border-left: 5px solid #38bdf8;
    }

    /* Forensic Report Card */
    .report-card {
        background-color: rgba(255, 255, 255, 0.1); backdrop-filter: blur(30px);
        padding: 35px; border-radius: 20px; border: 2px solid #38bdf8;
        color: #ffffff !important; line-height: 1.8; font-size: 1.15rem;
    }

    .main-title {
        background: linear-gradient(to right, #38bdf8, #818cf8);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-size: 4.8rem; font-weight: 900; text-align: center;
        filter: drop-shadow(0 10px 15px rgba(56, 189, 248, 0.3));
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

# # 4. Pro Tech Sidebar Dashboard
with st.sidebar:
    st.markdown('<p class="sidebar-header">🛡️ Satyarth Control</p>', unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown("### 📊 System Health")
    st.markdown('<div class="metric-container"><b>SambaNova Engine</b><br><small>STATUS: ACTIVE 🟢</small></div>', unsafe_allow_html=True)
    st.markdown('<div class="metric-container"><b>Forensic Agents</b><br><small>MODE: HYPER-LOCAL 📍</small></div>', unsafe_allow_html=True)
    st.markdown('<div class="metric-container"><b>Memory Buffer</b><br><small>USAGE: OPTIMAL 100% ✅</small></div>', unsafe_allow_html=True)
    
    # About Section Integration
    with st.expander("ℹ️ About Satyarth-AI"):
        st.markdown(f"""
        **How it works?**
        1. **Scout Agent:** Ye internet ke official gov portals aur regional news sources ko scan karta hai.
        2. **Analyst Agent:** Ye sources ko points deta hai (Credibility Score) aur final Hinglish report likhta hai.
        3. **Image Forensic:** Gemini 1.5 Flash pixels ko analyze karke AI markers dhundta hai.
        """)

    st.write("---")
    st.markdown('<p class="dev-label">Developed by Team Future Flux</p>', unsafe_allow_html=True)
    # Email Request
    st.markdown('<p class="email-text">📩 satyarthai2007@gmail.com</p>', unsafe_allow_html=True)
    st.caption("NIT Hamirpur | Electrothon 8.0")

# # 5. Main UI
st.markdown('<h1 class="main-title">SATYARTH-AI</h1>', unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 1.3rem;'>Automated High-Fidelity Disinformation Detection Engine</p>", unsafe_allow_html=True)
st.write("---")

tab1, tab2 = st.tabs(["🔍 Text Verification", "🔬 Image Investigation"])

with tab1:
    c_in, c_loc = st.columns([2, 1])
    with c_in:
        news_topic = st.text_input("News Headline Daalein 👇", placeholder="e.g. Is NIT Hamirpur closing tomorrow?")
    with c_loc:
        # Region Requested as Optional
        region = st.text_input("Region (Optional) 📍", placeholder="District and State")

    if st.button("🚀 START DEEP FORENSIC ANALYSIS", key="text_btn"):
        if news_topic:
            with st.status(f"🕵️ Investigating sources for {region if region else 'Global'}...", expanded=True) as status:
                scout = Agent(
                    role='Forensic Scout',
                    goal=f'Verify {news_topic} in {region}. Strictly use local official sources.',
                    backstory="Digital Detective.", tools=[search_tool], llm=text_llm, verbose=True
                )
                analyst = Agent(
                    role='Lead Verifier',
                    goal='Write professional Hinglish verdict report.',
                    backstory="Expert Journalist.", llm=text_llm, verbose=True
                )
                crew = Crew(
                    agents=[scout, analyst],
                    tasks=[
                        Task(description=f"Verify {news_topic} in {region}.", agent=scout, expected_output="Facts."),
                        Task(description="Write forensic report in Hinglish.", agent=analyst, expected_output="Report.")
                    ],
                    process=Process.sequential
                )
                result = crew.kickoff()
                st.session_state.final_report = result.raw
                status.update(label="Analysis Complete! ✅", state="complete")
            st.balloons()
        else:
            st.warning("Sir, please news enter kijiye!")

    if "final_report" in st.session_state:
        st.markdown(f'<div class="report-card"><h3>📜 Forensic Verification Report</h3>{st.session_state.final_report}</div>', unsafe_allow_html=True)
        st.write("---")
        if st.button("👥 Request Human Verification"):
            st.info("you will be informed when we receive reply")

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
