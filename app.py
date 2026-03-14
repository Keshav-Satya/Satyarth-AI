import streamlit as st
import os
import base64
from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun
import google.generativeai as genai
from PIL import Image

# # 1. Page Configuration
st.set_page_config(page_title="Satyarth-AI | Multimodal", page_icon="🛡️", layout="wide")

# # 2. Advanced Professional CSS (Cyber-Security Theme)
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

# # 3. API Keys Verification
if "SAMBANOVA_API_KEY" not in st.secrets or "GOOGLE_API_KEY" not in st.secrets:
    st.error("Sir, please Secrets mein SAMBANOVA_API_KEY aur GOOGLE_API_KEY dono daaliye!")
    st.stop()

# # 4. Initialize Models (SambaNova for Text)
text_llm = LLM(
    model="openai/meta-llama/Llama-3.3-70B-Instruct",
    base_url="https://api.sambanova.ai/v1",
    api_key=st.secrets["SAMBANOVA_API_KEY"],
    temperature=0.1
)

# # 5. Search Tool (Optimized for Tokens)
@tool('search_tool')
def search_tool(query: str):
    """Search internet for official and local news facts."""
    search = DuckDuckGoSearchRun()
    # Token saving logic (200 characters)
    return search.run(query)[:200]

# # 6. Sidebar Configuration
with st.sidebar:
    st.markdown("# 🛡️ Satyarth-AI")
    st.success("✅ System: Multimodal Active")
    st.write("---")
    st.write("Developed by **Team Future Flux** | NIT Hamirpur")

# # 7. Main Dashboard
st.markdown('<h1 class="main-title">🛡️ Satyarth-AI</h1>', unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Advanced Disinformation Detection & Image Forensic Engine</p>", unsafe_allow_html=True)
st.write("---")

tab1, tab2 = st.tabs(["📝 Text Verification", "📸 Image Investigation"])

# --- TAB 1: Text Investigation (Local/Official News + Animations) ---
with tab1:
    news_topic = st.text_input("Sir, kis news ka 'Parda-Faash' karna hai?", placeholder="e.g. Is viral NASA photo real?")
    location = st.text_input("Location (e.g. Mandi, Hamirpur, Himachal ya Global)", value="Global")
    
    if st.button("Satyarth Analysis Shuru Karein", type="primary"):
        if news_topic:
            with st.status("🔍 Searching & Analyzing Data...", expanded=True) as status:
                st.write("🌐 Initializing Forensic Agents...")

                # Agent 1: Regional Scout (Official First Logic)
                scout = Agent(
                    role='Official & Regional Scout',
                    goal=f'Verify facts for: {news_topic} in {location}. Prioritize .gov sites and local portals.',
                    backstory=f"Aap ek detective hain jo {location} ke official documents aur local news se sachai nikaalte hain. Har fact ke saath URL link collect karein.",
                    tools=[search_tool],
                    llm=text_llm,
                    verbose=True
                )

                # Agent 2: Forensic Analyst (Scoring & Sources)
                analyst = Agent(
                    role='Forensic Analyst',
                    goal='Final forensic report in Hinglish. MUST include Credibility Score (%) and "Sources Used" links.',
                    backstory="Aap government sources ko 50% priority dete hain aur final report mein saare links (URLs) show karte hain.",
                    llm=text_llm,
                    verbose=True
                )

                task1 = Task(description=f"Find current facts and evidence for: {news_topic} in {location}.", agent=scout, expected_output="List of verified facts and URLs.")
                task2 = Task(description="Synthesize findings into a Hinglish report with Score Card and Sources.", agent=analyst, expected_output="Final Forensic Report.")

                crew = Crew(agents=[scout, analyst], tasks=[task1, task2], process=Process.sequential)
                result = crew.kickoff()
                
                status.update(label="Investigation Complete! ✅", state="complete")
                
                # --- Result Display & Animations ---
                st.markdown(f'<div class="report-card"><h3>📜 Satyarth Forensic Report</h3>{result.raw}</div>', unsafe_allow_html=True)
                
                verdict_lower = result.raw.lower()
                # Party Vibe for True News
                if any(word in verdict_lower for word in ["real", "true", "verified", "sahi", "authentic"]):
                    st.success("🎉 Mubaarak ho Sir! Ye news Sacchi hai.")
                    st.balloons()
                # Sad Vibe for Fake News
                elif any(word in verdict_lower for word in ["fake", "false", "misleading", "galat", "fraud"]):
                    st.error("🚨 Savdhaan Sir! Ye news Fake hai.")
                    st.snow()
                else:
                    st.info("Sir, report inconclusive hai. Sources check karein.")
        else:
            st.warning("Sir, please ek news topic enter kijiye!")

# --- TAB 2: Image Investigation (Gemini Flash) ---
with tab2:
    st.info("Sir, yahan aap Live Photo khinch sakte hain ya File upload kar sakte hain!")
    cam_on = st.toggle("📸 Camera On/Off Karein", value=False)
    
    col1, col2 = st.columns(2)
    with col1:
        img_file = st.file_uploader("Investigation ke liye photo upload karein", type=['jpg', 'png', 'jpeg'])
    with col2:
        cam_file = st.camera_input("Live Photo click karein") if cam_on else st.write("👈 Camera off hai.")

    final_img = img_file or cam_file
    
    if final_img:
        st.image(final_img, caption="Scan ke liye image taiyar hai.", width=400)
        if st.button("AI Image Detection", key="img_btn"):
            with st.spinner("🔍 Forensic Sentinel scanning pixels..."):
                try:
                    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    img = Image.open(final_img)
                    response = model.generate_content(["Analyze image for AI markers. Verdict in Hinglish.", img])
                    st.markdown(f'<div class="report-card"><h3>🔍 Forensic Image Analysis</h3>{response.text}</div>', unsafe_allow_html=True)
                    if "real" in response.text.lower(): st.balloons()
                    else: st.snow()
                except Exception as e:
                    st.error(f"Sir, error: {e}")
