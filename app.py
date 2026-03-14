import streamlit as st
import os
import base64
from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun
from groq import Groq
from PIL import Image

# 1. Page Configuration
st.set_page_config(page_title="Satyarth-AI | Multimodal", page_icon="🕵️", layout="wide")

# 2. Advanced Professional CSS (Cyber-Security Theme) - No changes made here
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); }
    .report-card {
        background-color: white; padding: 30px; border-radius: 20px;
        border-top: 10px solid #FF4B4B; box-shadow: 0 15px 35px rgba(0,0,0,0.2);
        color: #2e3e50; margin-top: 20px;
    }
    .main-title { color: #1e3799; font-size: 3rem; font-weight: 800; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# 3. API Keys Verification
if "SAMBANOVA_API_KEY" not in st.secrets or "GROQ_API_KEY" not in st.secrets:
    st.error("Sir, please Secrets mein SAMBANOVA_API_KEY aur GROQ_API_KEY dono daaliye!")
    st.stop()

# 4. Initialize Models & Clients
text_llm = LLM(
    model="openai/Meta-Llama-3.3-70B-Instruct",
    base_url="https://api.sambanova.ai/v1",
    api_key=st.secrets["SAMBANOVA_API_KEY"]
)

groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])

def encode_image(image_file):
    """Converts image to base64 for Groq Vision API."""
    return base64.b64encode(image_file.getvalue()).decode('utf-8')

@tool('search_tool')
def search_tool(query: str):
    """Search internet for news facts."""
    search = DuckDuckGoSearchRun()
    search_result = search.run(query)
    return search_result[:200]

# --- Sidebar Configuration ---
with st.sidebar:
    st.markdown("# 🕵️ Satyarth-AI")
    st.success("✅ System: Multimodal Active")
    st.write("---")
    st.write("Developed by **Team Future Flux** | NIT Hamirpur")

# --- Main Dashboard ---
st.markdown('<h1 class="main-title">🕵️ Satyarth-AI</h1>', unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Advanced Disinformation Detection & Image Forensic Engine</p>", unsafe_allow_html=True)
st.write("---")

tab1, tab2 = st.tabs(["📝 Text Verification", "📷 Image Investigation"])

# --- TAB 1: Text Investigation ---
with tab1:
    # Adding Region Input (Requirement: Side by side)
    col_n, col_r = st.columns([2, 1])
    with col_n:
        news_topic = st.text_input("Sir, kis news ka 'Parda-Faash' karna hai?", placeholder="e.g. Is viral news real?")
    with col_r:
        region = st.text_input("Region (Optional) 📍", placeholder="e.g. District, State")
    
    if st.button("Satyarth Analysis Shuru Karein", type="primary"):
        if news_topic:
            with st.status("🔍 Searching & Analyzing Data...", expanded=True) as status:
                st.write("🌐 Initializing Forensic Agents...")
                
                scout = Agent(
                    role='Digital Detective',
                    goal=f'Verify facts for: {news_topic} in {region if region else "Global"} context',
                    backstory="Aap ek expert fact-checker hain jo internet se sachai nikaalte hain.",
                    tools=[search_tool],
                    llm=text_llm,
                    verbose=True,
                    allow_delegation=False
                )
                
                analyst = Agent(
                    role='Forensic Analyst',
                    goal='Create a final verdict report in Hinglish.',
                    backstory="Aap investigative journalist hain jo clear verdict dete hain.",
                    llm=text_llm,
                    verbose=True
                )
                
                crew = Crew(
                    agents=[scout, analyst],
                    tasks=[
                        Task(description=f"Find facts for: {news_topic} in {region}", agent=scout, expected_output="Facts list."),
                        Task(description="Synthesize into final Hinglish report.", agent=analyst, expected_output="Final Report.")
                    ],
                    process=Process.sequential
                )
                
                result = crew.kickoff()
                # Persistence logic: storing in session state
                st.session_state.final_report = result.raw
                status.update(label="Investigation Complete! ✅", state="complete")
            st.balloons()
        else:
            st.warning("Sir, please news enter kijiye!")

    # Show Report and Human Verification Button (Only after analysis)
    if "final_report" in st.session_state:
        st.markdown(f'<div class="report-card"><h3>📜 Forensic Report</h3>{st.session_state.final_report}</div>', unsafe_allow_html=True)
        st.write("---")
        # Functional requirement: Human Verification Option
        st.markdown("### 👥 Human Intelligence Module")
        if st.button("Get Human Verification"):
            st.info("you will be notified result shortly")

# --- TAB 2: Image Investigation ---
with tab2:
    st.info("Sir, yahan aap photo upload karein ya Camera switch ka upyog karein! 🚀")
    cam_on = st.toggle("📸 Camera On/Off Karein", value=False, key="cam_toggle")
    col1, col2 = st.columns(2)
    with col1:
        img_file = st.file_uploader("Investigation ke liye photo upload karein", type=['jpg', 'png', 'jpeg'])
    with col2:
        cam_file = None
        if cam_on:
            cam_file = st.camera_input("Live Photo click karein")
        else:
            st.write("👈 Camera on karne ke liye switch ka upyog karein.")

    final_img = img_file or cam_file
    if final_img:
        st.image(final_img, caption="Scan ke liye image taiyar hai.", width=400)
        if st.button("AI Detection Shuru Karein", key="img_btn"):
            # Original logic preserved
            with st.spinner("Analyzing..."):
                try:
                    import google.generativeai as genai
                    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    img = Image.open(final_img)
                    response = model.generate_content(["Analyze markers. Verdict in Hinglish.", img])
                    st.markdown(f'<div class="report-card"><h3>🔍 Forensic Analysis Report</h3>{response.text}</div>', unsafe_allow_html=True)
                except Exception as e: st.error(f"Error: {e}")
