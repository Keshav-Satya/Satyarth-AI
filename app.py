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

# # 2. Premium "Deep Indigo" UI (Replacing Black)
st.markdown("""
    <style>
    /* Premium Space Gradient Background */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #f1f5f9;
    }
    
    /* Glassmorphism Cards */
    .report-card {
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 30px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5);
        margin-top: 20px;
    }

    /* Vibrant Gradient Title */
    .main-title {
        background: linear-gradient(to right, #38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.8rem;
        font-weight: 900;
        text-align: center;
        text-shadow: 0 10px 20px rgba(0,0,0,0.3);
    }

    /* Buttons with Glow */
    .stButton>button {
        background: linear-gradient(45deg, #0284c7, #4f46e5);
        color: white;
        border: none;
        padding: 12px 30px;
        border-radius: 12px;
        font-weight: 600;
        transition: 0.3s;
    }
    .stButton>button:hover {
        box-shadow: 0 0 25px rgba(56, 189, 248, 0.6);
        transform: translateY(-2px);
    }
    </style>
    """, unsafe_allow_html=True)

# # 3. API Keys Check
if "SAMBANOVA_API_KEY" not in st.secrets or "GOOGLE_API_KEY" not in st.secrets:
    st.error("Sir, please Secrets mein Keys check karein!")
    st.stop()

# # 4. Engine Setup
text_llm = LLM(
    model="openai/meta-llama/Llama-3.3-70B-Instruct",
    base_url="https://api.sambanova.ai/v1",
    api_key=st.secrets["SAMBANOVA_API_KEY"],
    temperature=0.1
)

@tool('search_tool')
def search_tool(query: str):
    """Search tools with token protection."""
    search = DuckDuckGoSearchRun()
    return search.run(query)[:250]

# # 5. Sidebar Dashboard
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>🛡️ Satyarth-AI</h2>", unsafe_allow_html=True)
    st.write("---")
    st.metric("Engine Status", "Active 🟢")
    st.info("📡 SambaNova: Connected")
    st.info("💠 Gemini Vision: Ready")
    st.write("---")
    st.markdown("Developed by **Team Future Flux**")

# # 6. Header
st.markdown('<h1 class="main-title">SATYARTH-AI</h1>', unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8;'>Hyper-Local Disinformation Detection & Image Forensic Engine</p>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🔍 Text Verification", "🔬 Image Investigation"])

# --- TAB 1: Text ---
with tab1:
    col_in1, col_in2 = st.columns([3, 1])
    with col_in1: news_topic = st.text_input("News headline daalein...", placeholder="e.g. Is NIT Hamirpur closing?")
    with col_in2: location = st.text_input("Location", value="Global")

    if st.button("🚀 Start Deep Forensic Analysis"):
        if news_topic:
            with st.status("🕵️ Investigating...", expanded=True) as status:
                scout = Agent(role='Data Scout', goal=f'Verify {news_topic} in {location}.', backstory="Expert in .gov and local news.", tools=[search_tool], llm=text_llm)
                analyst = Agent(role='Forensic Analyst', goal='Hinglish report with Score Card.', backstory="Weighted scoring expert.", llm=text_llm)
                crew = Crew(agents=[scout, analyst], tasks=[Task(description=f"Check {news_topic}", agent=scout, expected_output="Facts"), Task(description="Report", agent=analyst, expected_output="Report")], process=Process.sequential)
                result = crew.kickoff()
                status.update(label="Complete! ✅", state="complete")
                st.markdown(f'<div class="report-card"><h3>📜 Forensic Report</h3>{result.raw}</div>', unsafe_allow_html=True)
                if any(x in result.raw.lower() for x in ["real", "true", "sahi"]): st.balloons()
                elif any(x in result.raw.lower() for x in ["fake", "false", "galat"]): st.snow()

# --- TAB 2: Image Investigation (Error Fixed Here) ---
with tab2:
    st.markdown("### 📸 Image Forensic Module")
    cam_toggle = st.toggle("🎥 Activate Live Camera Feed", value=False)
    
    col_up1, col_up2 = st.columns(2)
    img_cam = None # Initialize as None
    
    with col_up1:
        img_upload = st.file_uploader("Upload Image", type=['jpg', 'png', 'jpeg'])
    with col_up2:
        if cam_toggle:
            img_cam = st.camera_input("Take Photo")
        else:
            st.info("Camera is currently OFF.")

    # Fix logic: only consider if it's a valid file object
    final_image = img_upload if img_upload is not None else img_cam
    
    if final_image is not None:
        st.image(final_image, caption="Investigating Image...", width=400)
        if st.button("🔍 Run Image Forensic Scan"):
            with st.spinner("Analyzing pixels..."):
                try:
                    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    img_obj = Image.open(final_image)
                    response = model.generate_content(["Analyze image for AI markers. Hinglish Verdict.", img_obj])
                    st.markdown(f'<div class="report-card"><h3>🔬 Image Verdict</h3>{response.text}</div>', unsafe_allow_html=True)
                    if "real" in response.text.lower(): st.balloons()
                    else: st.snow()
                except Exception as e:
                    st.error(f"Error: {e}")
