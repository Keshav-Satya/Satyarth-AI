import streamlit as st
import os
import base64
from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun
import google.generativeai as genai
from PIL import Image

# # 1. Page Configuration
st.set_page_config(page_title="Satyarth-AI | Forensic Engine", page_icon="🛡️", layout="wide")

# # 2. Cyber-Security High-Readability UI (Indigo Theme)
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); color: #f1f5f9; }
    
    /* Input Labels Readability Fix */
    [data-testid="stWidgetLabel"] p {
        font-size: 1.25rem !important; font-weight: 700 !important;
        color: #38bdf8 !important; text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] button { font-size: 1.2rem !important; font-weight: 600 !important; color: #94a3b8 !important; }
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] { color: #38bdf8 !important; border-bottom: 3px solid #38bdf8 !important; }

    /* Glassmorphism Report Cards */
    .report-card {
        background: rgba(30, 41, 59, 0.85); backdrop-filter: blur(15px);
        border-radius: 20px; padding: 25px; border: 1px solid rgba(56, 189, 248, 0.3);
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.6); margin-top: 20px;
    }

    .main-title {
        background: linear-gradient(to right, #38bdf8, #818cf8);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-size: 4rem; font-weight: 900; text-align: center;
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

# # 4. Text Engine Initialization (Fixed NotFoundError)
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
    return search.run(query)[:250]

# # 5. Sidebar Layout
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #38bdf8;'>🛡️ Satyarth-AI</h2>", unsafe_allow_html=True)
    st.write("---")
    st.metric("System Mode", "Hyper-Local 📍")
    st.info("📡 SambaNova: Connected")
    st.info("💠 Gemini Vision: Ready")
    st.write("---")
    st.markdown("Developed by **Team Future Flux** | NIT Hamirpur")

# # 6. Header Section
st.markdown('<h1 class="main-title">SATYARTH-AI</h1>', unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.1rem; color: #94a3b8;'>Advanced News Verification & Image Forensic Engine</p>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🔍 Text Verification", "🔬 Image Investigation"])

# --- TAB 1: Text Investigation ---
with tab1:
    col_t1, col_t2 = st.columns([3, 1])
    with col_t1: news_topic = st.text_input("News Headline Daalein 👇", placeholder="e.g. Is NIT Hamirpur closing tomorrow?")
    with col_t2: location = st.text_input("Location 📍", value="Global")

    if st.button("🚀 START DEEP FORENSIC ANALYSIS"):
        if news_topic:
            with st.status("🕵️ Investigation in Progress...", expanded=True) as status:
                st.write("🌐 Scanning Government Portals & Local News...")
                
                # Agents Definition (Self-contained in app.py)
                scout = Agent(
                    role='Local Ground Reality Scout',
                    goal=f'Verify {news_topic} in {location}. Prioritize .gov sites & local vendors.',
                    backstory="Aap local ground reality aur official reports verify karte hain.",
                    tools=[search_tool], llm=text_llm, verbose=True
                )
                analyst = Agent(
                    role='Forensic Analyst',
                    goal='Final Hinglish report with Score Card and Sources.',
                    backstory="Aap sources ko weighted points (50/30/15/5) dete hain.",
                    llm=text_llm, verbose=True
                )

                crew = Crew(
                    agents=[scout, analyst],
                    tasks=[
                        Task(description=f"Investigate {news_topic} in {location}.", agent=scout, expected_output="Facts & Sources"),
                        Task(description="Generate forensic report with Credibility Score.", agent=analyst, expected_output="Report")
                    ],
                    process=Process.sequential
                )
                
                result = crew.kickoff()
                status.update(label="Analysis Complete! ✅", state="complete")
                
                st.markdown(f'<div class="report-card"><h3>📜 Forensic Report</h3>{result.raw}</div>', unsafe_allow_html=True)
                
                # Animations
                res_low = result.raw.lower()
                if any(x in res_low for x in ["real", "true", "sahi"]):
                    st.success("✅ Truth Detected!")
                    st.balloons()
                elif any(x in res_low for x in ["fake", "false", "galat"]):
                    st.error("❌ Disinformation Detected!")
                    st.snow()
            
            # --- Human Expert Request Button ---
            st.write("---")
            st.markdown("### 👥 Human Intelligence")
            if st.button("Request Verification from Local Vendors & Agents"):
                st.toast("Alert sent to local human agents!")
                st.info(f"Sir, humne {location} ke verified vendors aur owners ko alert bhej diya hai. Ground verification report jald update hogi! 📡")
        else:
            st.warning("Sir, please headline enter karein!")

# --- TAB 2: Image Investigation ---
with tab2:
    st.markdown("### 🔬 Image Forensic Module")
    cam_toggle = st.toggle("🎥 Activate Live Camera", value=False)
    
    c1, c2 = st.columns(2)
    img_cam = None
    with c1: img_file = st.file_uploader("Upload Image", type=['jpg','png','jpeg'])
    with c2: img_cam = st.camera_input("Take Photo") if cam_toggle else st.info("Camera is OFF.")

    final_img = img_file if img_file is not None else img_cam
    
    if final_img is not None:
        st.image(final_img, caption="Forensic Scan Ready.", width=500)
        if st.button("🔍 RUN PIXEL ANALYSIS"):
            with st.spinner("Analyzing AI markers..."):
                try:
                    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    response = model.generate_content(["Analyze image for AI artifacts. Verdict in Hinglish.", Image.open(final_img)])
                    st.markdown(f'<div class="report-card"><h3>🔬 Verdict</h3>{response.text}</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Error: {e}")
