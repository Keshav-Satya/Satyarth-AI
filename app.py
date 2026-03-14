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

@tool('search_tool')
def search_tool(query: str):
    """Search internet for news facts with extreme token saving."""
    search = DuckDuckGoSearchRun()
    # Sir, 200 characters fact-checking ke main context ke liye kaafi hain
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

# --- TAB 1: Text Investigation (CrewAI Power) ---
with tab1:
    news_topic = st.text_input("Sir, kis news ka 'Parda-Faash' karna hai?", placeholder="e.g. Is viral NASA photo real?")
    # Line 70 ke niche ye line add karein
 location = st.text_input("Location (e.g. Mandi, Hamirpur, Himachal ya Global)", value="Global")
    if st.button("Satyarth Analysis Shuru Karein", type="primary"):
        if news_topic:
            with st.status("🔍 Searching & Analyzing Data...", expanded=True) as status:
                st.write("🌐 Initializing Forensic Agents...")
                
               # Agent 1: Regional Scout (Line 78 onwards)
        scout = Agent(
            role='Regional Information Scout',
            goal=f'Verify facts for: {news_topic} in {location} context and collect source website links.',
            backstory=f"Aap ek expert detective hain jo {location} ke local portals (jaise Amar Ujala, Tribune) aur official records se sachai nikaalte hain. Aapko har fact ke saath uska URL link bhi collect karna hai.",
            tools=[search_tool],
            llm=text_llm,
            verbose=True,
            allow_delegation=False
        )

        # Agent 2: Forensic Analyst (Line 88 onwards)
        analyst = Agent(
            role='Forensic News Verifier',
            goal='Create a final forensic report in Hinglish. MUST include a "Sources Used" section with links at the end.',
            backstory="Aap ek senior investigative journalist hain. Aap sources ki credibility check karte hain aur final verdict ke saath un websites ke links dete hain jahan se information li gayi hai.",
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

# --- TAB 2: Image Investigation (With Camera Toggle) ---
with tab2:
    st.info("Sir, yahan aap photo upload karein ya Camera switch ka upyog karein! 🚀")
    
    # 1. Camera Toggle Switch
    cam_on = st.toggle("📸 Camera On/Off Karein", value=False, key="cam_toggle")

    col1, col2 = st.columns(2)
    
    with col1:
        img_file = st.file_uploader("Investigation ke liye photo upload karein", type=['jpg', 'png', 'jpeg'])
    
    with col2:
        cam_file = None
        # Agar switch 'On' hai, tabhi camera input dikhao
        if cam_on:
            cam_file = st.camera_input("Live Photo click karein")
        else:
            st.write("👈 Camera on karne ke liye switch ka upyog karein.")

    # Input Priority (Upload ya Camera)
    final_img = img_file or cam_file
    
    if final_img:
        st.image(final_img, caption="Scan ke liye image taiyar hai.", width=400)
        
        if st.button("AI Detection Shuru Karein", key="img_btn"):
            if "GOOGLE_API_KEY" not in st.secrets:
                st.error("Sir, please Secrets mein GOOGLE_API_KEY daaliye!")
            else:
                with st.spinner("🔍 Forensic Sentinel is analyzing the pixels..."):
                    try:
                        import google.generativeai as genai
                        from PIL import Image
                        
                        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
                        
                        # Active model dhoondne ki logic
                        all_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                        working_model_name = next((p for p in ['models/gemini-1.5-flash', 'models/gemini-1.5-pro'] if p in all_models), None)

                        if working_model_name:
                            model = genai.GenerativeModel(working_model_name)
                            img = Image.open(final_img)
                            prompt = "Analyze this image for AI generation markers. Verdict in Hinglish."
                            response = model.generate_content([prompt, img])
                            
                            st.markdown(f'<div class="report-card"><h3>🔍 Forensic Analysis Report</h3>{response.text}</div>', unsafe_allow_html=True)
                            st.balloons()
                        else:
                            st.error("Sir, koi vision model active nahi mila.")
                            
                    except Exception as e:
                        st.error(f"Sir, detection mein issue aaya: {e}")


