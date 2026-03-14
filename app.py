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

# 2. Advanced Professional CSS (Cyber-Security Theme)
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
# Text model (SambaNova - Llama 3.3)
text_llm = LLM(
    model="openai/Meta-Llama-3.3-70B-Instruct",
    base_url="https://api.sambanova.ai/v1",
    api_key=st.secrets["SAMBANOVA_API_KEY"]
)

# Groq Client for Vision
groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])

def encode_image(image_file):
    """Converts image to base64 for Groq Vision API."""
    return base64.b64encode(image_file.getvalue()).decode('utf-8')

# 5. Search Tool for Agents
@tool('search_tool')
def search_tool(query: str):
    """Search internet for latest news and facts."""
    return DuckDuckGoSearchRun().run(query)[:2000]

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

# --- TAB 1: Text Investigation (CrewAI Power) ---
with tab1:
    news_topic = st.text_input("Sir, kis news ka 'Parda-Faash' karna hai?", placeholder="e.g. Is viral NASA photo real?")
    
    if st.button("Satyarth Analysis Shuru Karein", type="primary"):
        if news_topic:
            with st.status("🔍 Searching & Analyzing Data...", expanded=True) as status:
                st.write("🌐 Initializing Forensic Agents...")
                
                # Agent 1: Fact Checker
                scout = Agent(
                    role='Digital Detective',
                    goal=f'Verify all facts related to: {news_topic}',
                    backstory="Aap ek expert fact-checker hain jo internet ke kone-kone se sachai nikaalte hain.",
                    tools=[search_tool],
                    llm=text_llm,
                    verbose=True,
                    allow_delegation=False
                )
                
                # Agent 2: Reporter
                analyst = Agent(
                    role='Forensic Analyst',
                    goal='Create a final verdict report in Hinglish.',
                    backstory="Aap ek senior investigative journalist hain jo news ki authenticity check karte hain.",
                    llm=text_llm,
                    verbose=True
                )
                
                # Orchestrate the Crew
                crew = Crew(
                    agents=[scout, analyst],
                    tasks=[
                        Task(description=f"Find current facts and evidence for: {news_topic}", agent=scout, expected_output="A list of verified facts."),
                        Task(description="Synthesize findings into a final Hinglish report with a clear verdict.", agent=analyst, expected_output="Final Hinglish verdict report.")
                    ],
                    process=Process.sequential
                )
                
                result = crew.kickoff()
                status.update(label="Investigation Complete! ✅", state="complete")
            
            st.markdown(f'<div class="report-card"><h3>📜 Forensic Report</h3>{result.raw}</div>', unsafe_allow_html=True)
            st.balloons()
        else:
            st.warning("Sir, please ek topic ya news headline enter kijiye!")

# --- TAB 2: Image Investigation (SambaNova Vision) ---
with tab2:
    st.info("Sir, yahan hum SambaNova Llama 3.2 Vision use kar rahe hain! 🚀")
    img_file = st.file_uploader("Photo Upload Karein", type=['jpg', 'png', 'jpeg'])

    if img_file:
        st.image(img_file, caption="Investigation ke liye image taiyar hai.", width=400)
        
        if st.button("AI Detection Shuru Karein", key="img_btn"):
            with st.spinner("🔍 Samba-Vision Sentinel is scanning pixels..."):
                try:
                    import requests
                    # 1. Image ko base64 mein convert karein
                    base64_image = encode_image(img_file)
                    
                    # 2. SambaNova Vision API Call
                    api_key = st.secrets["SAMBANOVA_API_KEY"]
                    url = "https://api.sambanova.ai/v1/chat/completions"
                    
                    headers = {
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json"
                    }

                    payload = {
                        "model": "Llama-3.2-11B-Vision-Instruct",
                        "messages": [
                            {
                                "role": "user",
                                "content": [
                                    {"type": "text", "text": "Analyze this image for AI generation markers (warped textures, lighting mismatch). Provide a Forensic Verdict in Hinglish."},
                                    {
                                        "type": "image_url",
                                        "image_url": {
                                            "url": f"data:image/jpeg;base64,{base64_image}"
                                        }
                                    }
                                ]
                            }
                        ],
                        "temperature": 0.1
                    }

                    response = requests.post(url, headers=headers, json=payload)
                    res_json = response.json()

                    if "choices" in res_json:
                        report = res_json['choices'][0]['message']['content']
                        st.markdown(f'<div class="report-card"><h3>🔍 Forensic Image Analysis</h3>{report}</div>', unsafe_allow_html=True)
                        st.balloons()
                    else:
                        st.error(f"SambaNova Error: {res_json.get('error', 'Unknown Error')}")

                except Exception as e:
                    st.error(f"Sir, Vision system mein issue aaya: {e}")
