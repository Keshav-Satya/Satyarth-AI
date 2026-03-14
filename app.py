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

# Purana code:
# vision_model = genai.GenerativeModel('gemini-1.5-flash')

# Naya Updated Code:
vision_model = genai.GenerativeModel('gemini-1.5-flash-8b')


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

# --- TAB 1: Text Investigation (Corrected Block) ---
with tab1:
    news_topic = st.text_input("Sir, kis news ka 'Parda-Faash' karna hai?", key="text_in")
    if st.button("Satyarth Analysis Shuru Karein", type="primary"):
        if news_topic:
            with st.status("🔍 Searching & Analyzing...", expanded=True) as status:
                st.write("🛡️ Initializing Satyarth Agents...")
                
                # Agent 1: Scout with Backstory
                scout = Agent(
                    role='Digital Detective',
                    goal=f'Verify facts for: {news_topic}',
                    backstory="Aap ek expert fact-checker hain jo internet ke kone-kone se sachai nikaalte hain.",
                    tools=[search_tool],
                    llm=text_llm,
                    verbose=True,
                    allow_delegation=False
                )
                
                # Agent 2: Analyst with Backstory
                analyst = Agent(
                    role='Forensic Analyst',
                    goal='Final Verdict and Report',
                    backstory="Aap ek senior investigative journalist hain jo news ki authenticity check karte hain.",
                    llm=text_llm,
                    verbose=True
                )

                # Tasks Setup
                task1 = Task(description=f"Find facts for: {news_topic}", agent=scout, expected_output="List of facts")
                task2 = Task(description="Prepare final report", agent=analyst, expected_output="Final verdict")

                crew = Crew(
                    agents=[scout, analyst], 
                    tasks=[task1, task2], 
                    process=Process.sequential,
                    verbose=True
                )
                
                st.write("🌐 Scanning global databases...")
                result = crew.kickoff()
                status.update(label="Investigation Complete! ✅", state="complete")
                
            st.markdown(f'<div class="report-card"><h3>📜 Forensic Report</h3>{result.raw}</div>', unsafe_allow_html=True)
            st.balloons()
        else:
            st.warning("Sir, please ek topic enter kijiye!")

# --- TAB 2: Image Investigation (Camera & Upload) ---
import base64
from groq import Groq

# 1. Initialize Groq Client
groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])

def encode_image(image_file):
    return base64.b64encode(image_file.getvalue()).decode('utf-8')

# --- TAB 2: Image Investigation ---
with tab2:
    st.info("Sir, yahan hum Llama 3.2 Vision (via Groq) use kar rahe hain jo Gemini se fast hai! 🚀")
    
    img_file = st.file_uploader("Photo Upload Karein", type=['jpg', 'png', 'jpeg'])
    
    if img_file:
        st.image(img_file, caption="Investigation ke liye image taiyar hai.", width=400)
        
        if st.button("AI Detection Shuru Karein"):
            with st.spinner("🔍 Image ke pixels analyze ho rahe hain (Groq Power)..."):
                try:
                    # Convert image to base64
                    base64_image = encode_image(img_file)
                    
                    # Call Groq Vision API
                    response = groq_client.chat.completions.create(
                        messages=[
                            {
                                "role": "user",
                                "content": [
                                    {"type": "text", "text": "Analyze this image carefully. Check for AI artifacts, distorted textures, or inconsistencies. Provide a Forensic Verdict in Hinglish."},
                                    {
                                        "type": "image_url",
                                        "image_url": {
                                            "url": f"data:image/jpeg;base64,{base64_image}",
                                        },
                                    },
                                ],
                            }
                        ],
                        model="llama-3.2-11b-vision-preview",
                    )
                    
                    result_text = response.choices[0].message.content
                    st.markdown(f'<div class="report-card"><h3>🔍 Image Analysis Report</h3>{result_text}</div>', unsafe_allow_html=True)
                    st.balloons()
                    
                except Exception as e:
                    st.error(f"Sir, Groq mein bhi kuch issue aaya: {e}")





