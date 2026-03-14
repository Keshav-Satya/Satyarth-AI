import streamlit as st
import os
from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun
import google.generativeai as genai
from PIL import Image

# 1. Page Configuration
st.set_page_config(page_title="Satyarth-AI | Multimodal", page_icon="🕵️", layout="wide")

# 2. Advanced CSS
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); }
    .report-card { 
        background-color: white; padding: 30px; border-radius: 20px; 
        border-top: 10px solid #FF4B4B; box-shadow: 0 15px 35px rgba(0,0,0,0.2); 
        color: #2c3e50; margin-top: 20px;
    }
    .main-title { color: #1e3799; font-size: 3rem; font-weight: 800; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# 3. API Keys Verification
if "SAMBANOVA_API_KEY" not in st.secrets or "GOOGLE_API_KEY" not in st.secrets:
    st.error("Sir, please Secrets mein SAMBANOVA_API_KEY aur GOOGLE_API_KEY dono daaliye!")
    st.stop()

# 4. LLMs Setup
# Text model (SambaNova)
text_llm = LLM(
    model="openai/Meta-Llama-3.3-70B-Instruct", 
    base_url="https://api.sambanova.ai/v1",
    api_key=st.secrets["SAMBANOVA_API_KEY"]
)

# Vision model (Gemini) - Specifically for Image Analysis
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
vision_model = genai.GenerativeModel('gemini-1.5-flash')

# 5. Search Tool
@tool('search_tool')
def search_tool(query: str):
    """Search internet for news facts."""
    return DuckDuckGoSearchRun().run(query)[:2000]

# --- Sidebar ---
with st.sidebar:
    st.markdown("# 🕵️ Satyarth-AI")
    st.success("✅ System: Multimodal Active")
    st.write("---")
    st.write("Developed by **Team Future Flux**")

# --- Main UI ---
st.markdown('<h1 class="main-title">🕵️ Satyarth-AI</h1>', unsafe_allow_html=True)
st.write("---")

# Creating Tabs for Text and Image
tab1, tab2 = st.tabs(["📝 Text Verification", "📸 Image Investigation"])

# --- TAB 1: Text Investigation ---
with tab1:
    news_topic = st.text_input("Sir, kis news ka 'Parda-Faash' karna hai?", key="text_in")
    if st.button("Satyarth Analysis Shuru Karein", type="primary"):
        with st.status("🔍 Searching & Analyzing...", expanded=True):
            scout = Agent(role='Detective', goal=f'Verify {news_topic}', tools=[search_tool], llm=text_llm, verbose=True)
            analyst = Agent(role='Analyst', goal='Final Verdict', llm=text_llm, verbose=True)
            crew = Crew(agents=[scout, analyst], tasks=[Task(description=f'Verify {news_topic}', agent=scout, expected_output="Facts"), Task(description='Final Report', agent=analyst, expected_output="Verdict")], verbose=True)
            result = crew.kickoff()
        st.markdown(f'<div class="report-card"><h3>📜 Report</h3>{result.raw}</div>', unsafe_allow_html=True)
        st.balloons()

# --- TAB 2: Image Investigation (Camera & Upload) ---
with tab2:
    st.info("Sir, yahan aap photo khinch kar ya upload karke check kar sakte hain ki woh AI generated hai ya nahi.")
    
    img_file = st.file_uploader("Photo Upload Karein", type=['jpg', 'png', 'jpeg'])
    camera_img = st.camera_input("Ya Camera se photo lein 📸")
    
    final_img = img_file if img_file else camera_img

    if final_img:
        st.image(final_img, caption="Investigation ke liye image taiyar hai.", width=400)
        if st.button("AI Detection Shuru Karein"):
            with st.spinner("🕵️ Image ke pixels analyze ho rahe hain..."):
                img = Image.open(final_img)
                prompt = """Analyze this image carefully. 
                1. Check for AI artifacts (distorted fingers, weird textures, background inconsistencies).
                2. Determine if it's likely AI generated or a real photograph.
                3. If there is text in the image, verify its authenticity.
                Provide a final Forensic Verdict in Hinglish."""
                
                response = vision_model.generate_content([prompt, img])
                
            st.markdown(f'<div class="report-card"><h3>🔍 Image Analysis Report</h3>{response.text}</div>', unsafe_allow_html=True)
            st.balloons()
