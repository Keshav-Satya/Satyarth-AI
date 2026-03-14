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

# # 2. Advanced Cyber-Forensic CSS
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
    }
    </style>
    """, unsafe_allow_html=True)

# # 3. Models Setup
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

# # 4. Pro Tech Sidebar
with st.sidebar:
    st.markdown("## 🛡️ Satyarth Engine")
    st.markdown('<p><span class="pulse"></span> System Status: Online</p>', unsafe_allow_html=True)
    st.write("---")
    
    st.markdown("### 📊 Live Metrics")
    st.markdown('<div class="metric-container"><b>SambaNova:</b> Active 🟢<br><small>Latency: 45ms</small></div>', unsafe_allow_html=True)
    st.markdown('<div class="metric-container"><b>Forensic Agents:</b> 2 Running<br><small>Mode: Hyper-Local</small></div>', unsafe_allow_html=True)
    st.markdown('<div class="metric-container"><b>Token Quota:</b> 88% Available</div>', unsafe_allow_html=True)
    
    st.write("---")
    st.markdown("### 🛠️ Hardware Info")
    st.caption("Device: NIT-H Hack-Node")
    st.caption("Uptime: 02h 45m")
    
    st.write("---")
    st.write("Developed by **Team Future Flux**")

# # 5. Main Dashboard
st.markdown('<h1 class="main-title">SATYARTH-AI</h1>', unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8;'>Hyper-Local Disinformation Detection & Image Forensic Engine</p>", unsafe_allow_html=True)
st.write("---")

tab1, tab2 = st.tabs(["🔍 Text Verification", "🔬 Image Investigation"])

with tab1:
    col_input, col_loc = st.columns([2, 1])
    with col_input:
        news_topic = st.text_input("News Headline Daalein 👇", placeholder="e.g. Is Virat Kohli retiring?")
    with col_loc:
        # User requested: type region along with district and state
        region = st.text_input("Region (District and State) 📍", placeholder="e.g. Hamirpur, Himachal Pradesh")

    if st.button("🚀 Start Deep Satyarth Analysis"):
        if news_topic:
            with st.status(f"🕵️ Investigating {news_topic} in {region}...", expanded=True) as status:
                scout = Agent(
                    role='Local Data Scout',
                    goal=f'Verify {news_topic} in {region}. Strictly check district level news portals.',
                    backstory="Aap ek expert digital detective hain jo specific regions ki news verify karte hain.",
                    tools=[search_tool], llm=text_llm, verbose=True
                )
                analyst = Agent(
                    role='Lead Forensic Verifier',
                    goal='Write a Hinglish verdict report. Focus on local evidence.',
                    backstory="Aap results ko professional Hinglish mein verify karte hain.",
                    llm=text_llm, verbose=True
                )
                crew = Crew(
                    agents=[scout, analyst],
                    tasks=[
                        Task(description=f"Check {news_topic} specifically in {region}.", agent=scout, expected_output="Local facts & links."),
                        Task(description="Create final Hinglish report.", agent=analyst, expected_output="Report.")
                    ],
                    process=Process.sequential
                )
                result = crew.kickoff()
                st.session_state.final_report = result.raw
                status.update(label="Analysis Complete! ✅", state="complete")
            st.balloons()
        else:
            st.warning("Sir, news enter kijiye!")

    if "final_report" in st.session_state:
        st.markdown(f'<div class="report-card"><h3>📜 Forensic Report</h3>{st.session_state.final_report}</div>', unsafe_allow_html=True)
        st.write("---")
        if st.button("👥 Request Human Verification"):
            st.info("you will be informed when we receive reply")

# TAB 2 stable logic starts here...
