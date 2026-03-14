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

# --- TAB 2: Image Investigation (The "Never-Fail" Gemini Flash) ---
with tab2:
    st.info("Sir, yahan hum Gemini 1.5 Flash use kar rahe hain jo sabse stable aur fast hai! 🚀")
    img_file = st.file_uploader("Investigation ke liye photo upload karein", type=['jpg', 'png', 'jpeg'])
    
    if img_file:
        st.image(img_file, caption="Scan ke liye image taiyar hai.", width=400)
        
        if st.button("AI Detection Shuru Karein", key="img_btn"):
            if "GOOGLE_API_KEY" not in st.secrets:
                st.error("Sir, please Secrets mein GOOGLE_API_KEY daaliye!")
            else:
                with st.spinner("🔍 Gemini Forensic Engine is scanning pixels..."):
                    try:
                        import google.generativeai as genai
                        from PIL import Image
                        
                        # Configuration
                        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
                        
                        # Stable Model: gemini-1.5-flash (No latest suffix)
                        model = genai.GenerativeModel('gemini-1.5-flash')
                        
                        # Convert uploaded file to PIL Image
                        img = Image.open(img_file)
                        
                        # Professional Forensic Prompt
                        prompt = """
                        Analyze this image for AI generation markers (warped textures, unnatural limbs, 
                        lighting inconsistencies, or AI artifacts). Give a final verdict in Hinglish 
                        stating if the image is 'Real' or 'AI Generated' with reasons.
                        """
                        
                        # Generation
                        response = model.generate_content([prompt, img])
                        
                        # Output
                        if response.text:
                            st.markdown(f'<div class="report-card"><h3>🔍 Forensic Image Analysis</h3>{response.text}</div>', unsafe_allow_html=True)
                            st.balloons()
                        else:
                            st.error("Sir, model ne koi output nahi diya. Dubara try karein.")
                            
                    except Exception as e:
                        # Fail-safe: Agar Flash fail ho, toh Flash-8B try karein (Backup)
                        try:
                            st.write("🔄 Trying Backup Model (Flash-8B)...")
                            model_backup = genai.GenerativeModel('gemini-1.5-flash-8b')
                            response = model_backup.generate_content([prompt, img])
                            st.markdown(f'<div class="report-card"><h3>🔍 Forensic Analysis (Backup)</h3>{response.text}</div>', unsafe_allow_html=True)
                            st.balloons()
                        except Exception as e2:
                            st.error(f"Sir, Gemini ke saare models down hain: {e2}")

