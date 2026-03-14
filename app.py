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

# # 2. Ultimate High-Contrast "Blue-Armor" CSS
st.markdown("""
    <style>
    /* Global Background - Deep Black */
    .stApp { background: #020617 !important; color: #ffffff !important; }
    
    /* Input Boxes - Blue Dibbe Fix */
    div[data-baseweb="input"] {
        background-color: #0f172a !important; /* Deep Blue Background */
        border: 2px solid #38bdf8 !important; /* Neon Blue Border */
        border-radius: 10px !important;
    }
    input {
        color: #ffffff !important; /* Pure White Text */
        font-weight: 700 !important;
    }
    ::placeholder { color: #94a3b8 !important; opacity: 1; }

    /* Green Labels - News & Region */
    [data-testid="stWidgetLabel"] p {
        font-size: 1.4rem !important; 
        font-weight: 900 !important; 
        color: #ffffff !important; 
        background: #16a34a !important; /* Solid Dark Green */
        padding: 8px 20px; 
        border-radius: 8px;
        display: inline-block; 
        margin-bottom: 15px !important;
        border: 2px solid #ffffff;
    }

    /* BUTTONS - Solid Colors for Visibility */
    .stButton>button {
        color: #ffffff !important; /* Text ALWAYS White */
        font-weight: 900 !important;
        font-size: 1.2rem !important;
        text-transform: uppercase;
        border-radius: 12px !important;
        padding: 15px 30px !important;
        border: 3px solid #ffffff !important;
        transition: 0.3s;
    }

    /* Start Analysis Button (Deep Navy Blue) */
    .main-btn .stButton>button {
        background: #1e40af !important; /* Solid Navy Blue */
    }

    /* Request Human Verification (Solid Vibrant Red) */
    .red-btn .stButton>button {
        background: #dc2626 !important; /* Solid Red */
    }

    .stButton>button:hover {
        transform: scale(1.05);
        filter: brightness(1.2);
    }

    /* Sidebar Readability Overhaul */
    [data-testid="stSidebar"] {
        background-color: #020617 !important;
        border-right: 3px solid #38bdf8;
    }
    .metric-container {
        background: #1e293b !important;
        padding: 18px; border-radius: 12px;
        border: 2px solid #38bdf8; margin-bottom: 18px;
    }
    .metric-container b, .metric-container small {
        color: #ffffff !important;
        text-shadow: 1px 1px 2px #000;
    }

    /* Title & Scanner Animations */
    .main-title {
        background: linear-gradient(90deg, #38bdf8, #ffffff, #38bdf8);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-size: 5rem; font-weight: 900; text-align: center;
        filter: drop-shadow(0 0 15px rgba(56, 189, 248, 1));
    }
    .scanner {
        width: 100%; height: 6px; background: #38bdf8;
        box-shadow: 0 0 20px #38bdf8; position: relative; overflow: hidden;
        margin-bottom: 25px; border-radius: 10px;
    }
    .scanner::after {
        content: ''; display: block; width: 250px; height: 100%;
        background: #ffffff; box-shadow: 0 0 35px #ffffff;
        position: absolute; animation: scan 2s linear infinite;
    }
    @keyframes scan { 0% { left: -250px; } 100% { left: 100%; } }

    /* About Section Text */
    .stExpander { border: 2px solid #38bdf8 !important; background: #0f172a !important; }
    .stExpander p, .stExpander li { color: #ffffff !important; font-weight: 700; }
    
    /* Footer/Team Info */
    .dev-info { color: #38bdf8 !important; font-weight: 900; font-size: 1.1rem; }
    .email-box { color: #ffffff !important; font-weight: 800; background: #2563eb; padding: 5px 15px; border-radius: 5px; border: 1px solid white; }
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
        st.markdown("""
        - **Scout Agent:** Gov portals aur news sites scan karta hai.
        - **Analyst Agent:** Hinglish forensic report likhta hai.
        - **Vision AI:** Pixels analyze karke AI markers dhundta hai.
        """)

    st.write("---")
    st.markdown('<p class="dev-info">Developed by Team Future Flux</p>', unsafe_allow_html=True)
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
        news_topic = st.text_input("News Headline Daalein 👇", placeholder="e.g. Is viral news authentic?")
    with col_loc:
        region = st.text_input("Region (Optional) 📍", placeholder="e.g. Hamirpur, Himachal Pradesh")

    st.markdown('<div class="main-btn">', unsafe_allow_html=True)
    if st.button("🚀 START DEEP FORENSIC ANALYSIS", key="text_btn"):
        if news_topic:
            with st.status("🕵️ Investigating sources...", expanded=True) as status:
                scout = Agent(role='Scout', goal=f'Verify {news_topic} in {region}.', backstory="Detective.", tools=[search_tool], llm=text_llm)
                analyst = Agent(role='Verifier', goal='Write professional Hinglish report.', backstory="Lead Analyst.", llm=text_llm)
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
        st.markdown
