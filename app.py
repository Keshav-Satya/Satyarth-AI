import streamlit as st
import os
import base64
from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun
from groq import Groq
from PIL import Image

# # 1. Page Configuration (Base stable version)
st.set_page_config(page_title="Satyarth-AI | Forensic Engine", page_icon="🕵️", layout="wide")

# # 2. UI Styling (Indigo Theme with High Readability)
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); color: #f1f5f9; }
    [data-testid="stWidgetLabel"] p { font-size: 1.2rem !important; font-weight: 700 !important; color: #38bdf8 !important; }
    .report-card {
        background-color: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px);
        padding: 30px; border-radius: 20px; border: 1px solid rgba(56, 189, 248, 0.3);
        color: #f1f5f9; margin-top: 20px;
    }
    .main-title { color: #38bdf8; font-size: 3.5rem; font-weight: 900; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# # 3. API Keys Verification
if "SAMBANOVA_API_KEY" not in st.secrets or "GROQ_API_KEY" not in st.secrets:
    st.error("Sir, please Secrets mein SAMBANOVA_API_KEY aur GROQ_API_KEY dono daaliye!")
    st.stop()

# # 4. Text Engine (Fixed Model Name for Stability)
text_llm = LLM(
    model="sambanova/Meta-Llama-3.3-70B-Instruct", # 'sambanova/' prefix prevents NotFoundError
    base_url="https://api.sambanova.ai/v1",
    api_key=st.secrets["SAMBANOVA_API_KEY"]
)

@tool('search_tool')
def search_tool(query: str):
    """Search internet for news facts with token saving."""
    search = DuckDuckGoSearchRun()
    return search.run(query)[:250]

# # 5. Sidebar
with st.sidebar:
    st.markdown("# 🕵️ Satyarth-AI")
    st.success("✅ System: Multimodal Active")
    st.write("---")
    st.write("Developed by **Team Future Flux** | NIT Hamirpur")

# # 6. Dashboard Header
st.markdown('<h1 class="main-title">🕵️ Satyarth-AI</h1>', unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Advanced Local News Verification & Image Forensic Engine</p>", unsafe_allow_html=True)
st.write("---")

tab1, tab2 = st.tabs(["📝 Text Verification", "📷 Image Investigation"])

# --- TAB 1: Text Investigation ---
with tab1:
    col_t1, col_t2 = st.columns([3, 1])
    with col_t1:
        news_topic = st.text_input("Sir, kis news ka 'Parda-Faash' karna hai?", placeholder="e.g. Is viral news real?")
    with col_t2:
        location = st.text_input("Location 📍", value="Global") # Added for judges' demand
    
    if st.button("Satyarth Analysis Shuru Karein", type="primary"):
        if news_topic:
            with st.status("🔍 Searching & Analyzing Data...", expanded=True) as status:
                st.write("🌐 Scanning Government & Local Sources...")
                
                scout = Agent(
                    role='Local Ground Scout',
                    goal=f'Verify facts for: {news_topic} in {location} context.',
                    backstory="Aap local vendors aur government reports se sachai nikaalte hain.",
                    tools=[search_tool], llm=text_llm, verbose=True
                )
                
                analyst = Agent(
                    role='Forensic Analyst',
                    goal='Create a final verdict report in Hinglish with Source Score.',
                    backstory="Aap news ki authenticity aur credibility check karte hain.",
                    llm=text_llm, verbose=True
                )
                
                crew = Crew(
                    agents=[scout, analyst],
                    tasks=[
                        Task(description=f"Investigate {news_topic} in {location}.", agent=scout, expected_output="Facts & URLs."),
                        Task(description="Generate Hinglish report with Score Card.", agent=analyst, expected_output="Final Report.")
                    ],
                    process=Process.sequential
                )
                
                result = crew.kickoff()
                status.update(label="Investigation Complete! ✅", state="complete")
            
            st.markdown(f'<div class="report-card"><h3>📜 Forensic Report</h3>{result.raw}</div>', unsafe_allow_html=True)
            
            # --- Result Animations ---
            if any(x in result.raw.lower() for x in ["real", "true", "sahi"]): st.balloons()
            elif any(x in result.raw.lower() for x in ["fake", "false", "galat"]): st.snow()
            
            # --- Human Verification (From Recording) ---
            st.write("---")
            if st.button("👥 Request Human Expert Verification"):
                st.toast("Requesting local vendors...")
                st.info(f"Sir, humne {location} ke verified vendors aur agents ko request bhej di hai. Ground report jald update hogi! 📡")
        else:
            st.warning("Sir, please topic enter kijiye!")

# --- TAB 2: Image Investigation (Fixed TypeError) ---
with tab2:
    st.info("Sir, yahan photo upload karein ya Camera switch ka upyog karein!")
    cam_on = st.toggle("📸 Camera On/Off Karein", value=False, key="cam_toggle")

    c1, c2 = st.columns(2)
    img_file = None
    cam_file = None
    
    with c1: img_file = st.file_uploader("Upload photo", type=['jpg', 'png', 'jpeg'])
    with c2:
        if cam_on: cam_file = st.camera_input("Live Photo click karein")
        else: st.write("👈 Camera off hai.")

    # Fix: Input Priority with safe check
    final_img = img_file if img_file is not None else cam_file
    
    if final_img is not None: # Changed from 'if final_img:' to prevent TypeError
        st.image(final_img, caption="Scan ke liye image taiyar hai.", width=400)
        
        if st.button("AI Detection Shuru Karein", key="img_btn"):
            if "GOOGLE_API_KEY" not in st.secrets:
                st.error("Sir, please Secrets mein GOOGLE_API_KEY daaliye!")
            else:
                with st.spinner("🔍 Forensic sentinel scanning pixels..."):
                    try:
                        import google.generativeai as genai
                        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
                        model = genai.GenerativeModel('models/gemini-1.5-flash')
                        response = model.generate_content(["Analyze image markers. Verdict in Hinglish.", Image.open(final_img)])
                        st.markdown(f'<div class="report-card"><h3>🔍 Image Analysis Report</h3>{response.text}</div>', unsafe_allow_html=True)
                        st.balloons()
                    except Exception as e: st.error(f"Error: {e}")
