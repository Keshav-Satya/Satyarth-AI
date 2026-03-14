import streamlit as st
import os
import base64
from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun
import google.generativeai as genai
from PIL import Image

# # 1. Page Configuration (The First Step)
st.set_page_config(page_title="Satyarth-AI | Forensic Engine", page_icon="🛡️", layout="wide")

# # 2. Cyber-Security Futuristic UI (CSS)
st.markdown("""
    <style>
    /* Global Styles */
    .stApp {
        background: radial-gradient(circle at center, #0e1117 0%, #000000 100%);
        color: #e0e0e0;
    }
    
    /* Glassmorphism Report Card */
    .report-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(12px);
        border-radius: 20px;
        padding: 30px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.8);
        margin-top: 20px;
    }

    /* Animated Gradient Title */
    .main-title {
        background: linear-gradient(90deg, #4facfe 0%, #00f2fe 50%, #4facfe 100%);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 4rem;
        font-weight: 900;
        text-align: center;
        animation: shine 3s linear infinite;
    }
    @keyframes shine { to { background-position: 200% center; } }

    /* Custom Buttons */
    .stButton>button {
        width: 100%;
        background: linear-gradient(45deg, #1e3799, #118ab2);
        color: white;
        border: none;
        padding: 15px;
        border-radius: 12px;
        font-weight: bold;
        transition: 0.4s;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 20px rgba(30, 55, 153, 0.4);
    }
    </style>
    """, unsafe_allow_html=True)

# # 3. API Keys Check
if "SAMBANOVA_API_KEY" not in st.secrets or "GOOGLE_API_KEY" not in st.secrets:
    st.error("Sir, please Secrets mein SAMBANOVA_API_KEY aur GOOGLE_API_KEY check karein!")
    st.stop()

# # 4. LLM & Tools Initialization
text_llm = LLM(
    model="openai/meta-llama/Llama-3.3-70B-Instruct",
    base_url="https://api.sambanova.ai/v1",
    api_key=st.secrets["SAMBANOVA_API_KEY"],
    temperature=0.1
)

@tool('search_tool')
def search_tool(query: str):
    """Search internet for official/local facts (200 char limit)."""
    search = DuckDuckGoSearchRun()
    return search.run(query)[:200]

# # 5. Sidebar Dashboard (Exciting UI)
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>🛡️ Satyarth-AI</h2>", unsafe_allow_html=True)
    st.write("---")
    st.markdown("### 📊 System Status")
    col_s1, col_s2 = st.columns(2)
    col_s1.metric("Engine", "Active 🟢")
    col_s2.metric("Forensic", "Mode 🛡️")
    
    st.info("📡 SambaNova: Connected")
    st.info("💠 Gemini Vision: Ready")
    
    st.write("---")
    st.markdown("Developed by **Team Future Flux**")
    st.caption("NIT Hamirpur | Electrothon 8.0")

# # 6. Header
st.markdown('<h1 class="main-title">SATYARTH-AI</h1>', unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #aaa;'>Hyper-Local Disinformation Detection & Image Forensic Engine</p>", unsafe_allow_html=True)
st.write("---")

tab1, tab2 = st.tabs(["🔍 Text Verification", "🔬 Image Investigation"])

# --- TAB 1: Text Investigation ---
with tab1:
    col_in1, col_in2 = st.columns([3, 1])
    with col_in1:
        news_topic = st.text_input("News headline daalein...", placeholder="e.g. Is NIT Hamirpur closing tomorrow?")
    with col_in2:
        location = st.text_input("Location", value="Global")

    if st.button("🚀 Start Deep Forensic Analysis"):
        if news_topic:
            with st.status("🕵️ Agents investigating the web...", expanded=True) as status:
                st.write("📡 Scanning Government Portals & Local News...")
                
                # Agents Logic (Official Priority)
                scout = Agent(
                    role='Official Data Scout',
                    goal=f'Verify {news_topic} in {location}. Prioritize .gov sites & local portals.',
                    backstory=f"Aap ek investigator hain jo {location} ke official links aur credible news portals scan karte hain.",
                    tools=[search_tool], llm=text_llm, verbose=True
                )
                analyst = Agent(
                    role='Forensic Analyst',
                    goal='Create a Hinglish report with Credibility Score (%) and Source Links.',
                    backstory="Aap government sources ko 50% weightage dete hain.",
                    llm=text_llm, verbose=True
                )

                crew = Crew(
                    agents=[scout, analyst],
                    tasks=[
                        Task(description=f"Investigate {news_topic} in {location} context.", agent=scout, expected_output="Facts & URLs"),
                        Task(description="Generate final Hinglish report with Score Card.", agent=analyst, expected_output="Final Report")
                    ],
                    process=Process.sequential
                )
                
                result = crew.kickoff()
                status.update(label="Analysis Complete! ✅", state="complete")

                # Results & Animations
                st.markdown(f'<div class="report-card"><h3>📜 Forensic Report</h3>{result.raw}</div>', unsafe_allow_html=True)
                
                res_text = result.raw.lower()
                if any(x in res_text for x in ["real", "true", "authentic", "sahi"]):
                    st.success("🎉 TRUTH DETECTED!")
                    st.balloons()
                elif any(x in res_text for x in ["fake", "false", "misleading", "galat"]):
                    st.error("🚨 WARNING: DISINFORMATION DETECTED!")
                    st.snow()
        else:
            st.warning("Sir, please enter a news topic first!")

# --- TAB 2: Image Investigation ---
with tab2:
    st.markdown("### 📸 Image Forensic Module")
    cam_toggle = st.toggle("🎥 Activate Live Camera Feed", value=False)
    
    col_up1, col_up2 = st.columns(2)
    with col_up1:
        img_upload = st.file_uploader("Upload Image", type=['jpg', 'png', 'jpeg'])
    with col_up2:
        img_cam = st.camera_input("Take Photo") if cam_toggle else st.info("Camera is currently OFF.")

    final_image = img_upload or img_cam
    if final_image:
        st.image(final_image, caption="Investigating Image...", width=400)
        if st.button("🔍 Run Image Forensic Scan"):
            with st.spinner("Analyzing pixels for AI artifacts..."):
                try:
                    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    img_obj = Image.open(final_image)
                    response = model.generate_content(["Analyze image for AI markers. Verdict in Hinglish.", img_obj])
                    st.markdown(f'<div class="report-card"><h3>🔬 Image Verdict</h3>{response.text}</div>', unsafe_allow_html=True)
                    if "real" in response.text.lower(): st.balloons()
                    else: st.snow()
                except Exception as e:
                    st.error(f"Error: {e}")
