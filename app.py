import streamlit as st
import os
from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun

# 1. Page Configuration
st.set_page_config(page_title="Satyarth-AI", page_icon="🕵️", layout="wide")

# 2. Block OpenAI
os.environ["OPENAI_API_KEY"] = "NA"

# 3. Native Gemini Setup - USING PRO VERSION (No 404 Error)
my_llm = LLM(
    model="gemini/gemini-1.5-pro", 
    api_key=st.secrets["GOOGLE_API_KEY"]
)

# 4. Search Tool Setup
@tool('search_tool')
def search_tool(query: str):
    """Search the internet for news and information."""
    search = DuckDuckGoSearchRun()
    return search.run(query)[:2000]

# --- UI Styling ---
st.markdown("""
    <style>
    .report-card { background-color: white; padding: 20px; border-radius: 15px; border-left: 5px solid #ff4b4b; color: black; }
    </style>
    """, unsafe_allow_html=True)

# --- Main App ---
st.title("🕵️ Satyarth-AI")
st.subheader("Deepfake & News Verifier")

news_topic = st.text_input("Sir, kis news ka 'Parda-Faash' karna hai?", placeholder="Viral topic yahan likhein...")
submit_button = st.button("Satyarth Investigation Shuru Karein", type="primary")

if submit_button and news_topic:
    with st.status("🔍 Investigation Shuru...", expanded=True) as status:
        st.write("🕵️ Agents charge up ho rahe hain...")
        
        # Agents
        scout = Agent(
            role='Digital Scout',
            goal=f'Verify facts for: {news_topic}',
            backstory="Aap ek expert fact-checker detective hain.",
            tools=[search_tool],
            llm=my_llm,
            verbose=True,
            allow_delegation=False
        )
        
        analyst = Agent(
            role='Forensic Analyst',
            goal='Prepare a final verdict report.',
            backstory="Aap ek senior investigative journalist hain.",
            llm=my_llm,
            verbose=True
        )

        # Tasks
        task1 = Task(description=f"Find facts for: {news_topic}", agent=scout, expected_output="Facts list")
        task2 = Task(description="Prepare final forensic report", agent=analyst, expected_output="Final verdict")

        # Crew - Sabse Stable Config
        satyarth_crew = Crew(
            agents=[scout, analyst],
            tasks=[task1, task2],
            process=Process.sequential,
            manager_llm=my_llm,
            memory=False, 
            verbose=True
        )

        st.write("🔍 Sources dhoonde ja rahe hain...")
        result = satyarth_crew.kickoff()
        status.update(label="Investigation Puri Hui! ✅", state="complete")

    st.markdown("### 📜 Final Forensic Report")
    st.markdown(f'<div class="report-card">{result.raw}</div>', unsafe_allow_html=True)
    st.balloons()
