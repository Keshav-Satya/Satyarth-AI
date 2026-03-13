import streamlit as st
import os
import time
from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun

# 1. Page Configuration
st.set_page_config(page_title="Satyarth-AI | Detective", page_icon="🕵️", layout="wide")

# 2. Force environment variables (Strictly Gemini)
os.environ["OPENAI_API_KEY"] = "NA" 
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("Sir, please Dashboard mein GOOGLE_API_KEY add kijiye!")
    st.stop()

# 3. Native CrewAI LLM Setup (Stable Version)
my_llm = LLM(
    model="gemini/gemini-1.5-flash", 
    api_key=st.secrets["GOOGLE_API_KEY"]
)

# 4. Search Tool
@tool('search_tool')
def search_tool(query: str):
    """Search the internet for news and information."""
    return DuckDuckGoSearchRun().run(query)[:2000]

# --- UI Styling ---
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .report-card { 
        background-color: white; 
        padding: 20px; 
        border-radius: 15px; 
        border-left: 5px solid #ff4b4b;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
        color: black;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2562/2562392.png", width=100)
    st.title("Satyarth Control Room")
    st.info("Sir, Satyarth-AI NIT Hamirpur ke liye taiyar hai.")

# --- Main UI ---
st.title("🕵️ Satyarth-AI")
st.subheader("Deepfake & News Verifier")

news_topic = st.text_input("Sir, aaj humein kis news ka 'Parda-Faash' karna hai?", placeholder="Viral news topic...")
submit_button = st.button("Satyarth Investigation Shuru Karein", type="primary")

if submit_button:
    if news_topic:
        with st.status("🔍 Investigation Shuru...", expanded=True) as status:
            st.write("🕵️ 1. Agents dimaag laga rahe hain...")
            
            scout = Agent(
                role='Digital Information Scout',
                goal=f'Verify facts for: {news_topic}',
                backstory="Aap ek fact-checker hain jo internet se sachai nikalte hain.",
                tools=[search_tool],
                llm=my_llm,
                verbose=True
            )

            analyst = Agent(
                role='News Verifier Analyst',
                goal='Analyze facts and give final verdict.',
                backstory="Aap ek investigative journalist hain jo final report taiyar karte hain.",
                llm=my_llm,
                verbose=True
            )

            task1 = Task(description=f"Search facts about: {news_topic}", agent=scout, expected_output="Facts list")
            task2 = Task(description="Prepare final forensic report", agent=analyst, expected_output="Final Report")

            # --- THE FIX: Embedder ko explicit specify karna ---
            satyarth_crew = Crew(
                agents=[scout, analyst],
                tasks=[task1, task2],
                process=Process.sequential,
                # Embedder ko specifically Gemini par set kar rahe hain
                embedder={
                    "provider": "google",
                    "config": {"model": "models/text-embedding-004", "api_key": st.secrets["GOOGLE_API_KEY"]}
                },
                verbose=True
            )

            st.write("🔍 2. Internet se sachai nikaali ja rahi hai...")
            result = satyarth_crew.kickoff()
            status.update(label="Investigation Puri Hui! ✅", state="complete", expanded=False)

        st.markdown("### 📜 Final Forensic Report")
        st.markdown(f'<div class="report-card">{result.raw}</div>', unsafe_allow_html=True)
        st.balloons()
    else:
        st.warning("Sir, please kuch topic likhiye!")
