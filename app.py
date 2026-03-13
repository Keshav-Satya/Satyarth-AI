import streamlit as st
import os
import time
from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun

# 1. Page Configuration
st.set_page_config(page_title="Satyarth-AI | Detective", page_icon="🕵️", layout="wide")

# 2. Environment Variables - Sabse pehle set karein
os.environ["OPENAI_API_KEY"] = "NA"
os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]

# 3. Native CrewAI LLM Setup
my_llm = LLM(
    model="gemini/gemini-1.5-flash",
    api_key=st.secrets["GOOGLE_API_KEY"]
)

# 4. Search Tool
@tool('search_tool')
def search_tool(query: str):
    """Search the internet for news and information."""
    return DuckDuckGoSearchRun().run(query)[:2000]

# --- UI Layout & Styling ---
st.markdown("""
    <style>
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

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2562/2562392.png", width=100)
    st.title("Satyarth Control Room")
    st.info("Sir, Satyarth-AI active hai aur investigation ke liye taiyar hai.")
    st.write("Developed by Team Future Flux")

st.title("🕵️ Satyarth-AI")
st.subheader("Deepfake & News Verifier")

news_topic = st.text_input("Sir, aaj humein kis news ka 'Parda-Faash' karna hai?", placeholder="Viral news topic...")
submit_button = st.button("Satyarth Investigation Shuru Karein", type="primary")

if submit_button:
    if news_topic:
        with st.status("🔍 Investigation Shuru...", expanded=True) as status:
            st.write("🕵️ Agents dimaag laga rahe hain...")
            
            scout = Agent(
                role='Digital Information Scout',
                goal=f'Verify facts for: {news_topic}',
                backstory="Expert fact-checker.",
                tools=[search_tool],
                llm=my_llm,
                verbose=True,
                allow_delegation=False
            )

            analyst = Agent(
                role='News Verifier Analyst',
                goal='Final verdict dena.',
                backstory="Senior investigative journalist.",
                llm=my_llm,
                verbose=True
            )

            task1 = Task(description=f"Find facts about: {news_topic}", agent=scout, expected_output="Facts list")
            task2 = Task(description="Prepare forensic report", agent=analyst, expected_output="Final Report")

            # --- FIX: Embedder Validation Error ka ilaj ---
            satyarth_crew = Crew(
                agents=[scout, analyst],
                tasks=[task1, task2],
                process=Process.sequential,
                # Humein embedder ki config ko bilkul waisa dena hai jaisa validation maang raha hai
                embedder={
                    "provider": "google-generativeai", # <--- 'google' ki jagah yeh zaroori hai
                    "config": {
                        "model": "models/embedding-001", 
                        "api_key": st.secrets["GOOGLE_API_KEY"]
                    }
                },
                verbose=True
            )

            st.write("🔍 Sources dhoonde ja rahe hain...")
            result = satyarth_crew.kickoff()
            status.update(label="Investigation Puri Hui! ✅", state="complete", expanded=False)

        st.markdown("### 📜 Final Forensic Report")
        st.markdown(f'<div class="report-card">{result.raw}</div>', unsafe_allow_html=True)
        st.balloons()
    else:
        st.warning("Sir, please kuch topic toh likhiye!")
