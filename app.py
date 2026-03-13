import streamlit as st
import os
import time
from crewai import Agent, Task, Crew, Process, LLM # Native LLM class
from crewai.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun

# 1. Page Configuration
st.set_page_config(page_title="Satyarth-AI | Detective", page_icon="🕵️", layout="wide")

# 2. OpenAI ko block karna (Startup crash se bachne ke liye)
os.environ["OPENAI_API_KEY"] = "NA"

# 3. Native CrewAI LLM Setup (Sabse stable tarika)
# Sir, hum key seedha yahan denge
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

# --- Main UI ---
st.title("🕵️ Satyarth-AI")
st.subheader("Deepfake & News Verifier")

news_topic = st.text_input("Sir, aaj humein kis news ka 'Parda-Faash' karna hai?", placeholder="Viral news topic...")
submit_button = st.button("Satyarth Investigation Shuru Karein", type="primary")

if submit_button:
    if news_topic:
        with st.status("🔍 Investigation Shuru...", expanded=True) as status:
            st.write("🕵️ Agents charge up ho rahe hain...")
            
            scout = Agent(
                role='Digital Information Scout',
                goal=f'Verify facts for: {news_topic}',
                backstory="Expert fact-checker detective.",
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

            task1 = Task(description=f"Search facts about: {news_topic}", agent=scout, expected_output="Facts list")
            task2 = Task(description="Prepare final forensic report", agent=analyst, expected_output="Final Report")

            # --- MASTER STROKE: Memory band kar rahe hain taaki 21 errors na aayein ---
            satyarth_crew = Crew(
                agents=[scout, analyst],
                tasks=[task1, task2],
                process=Process.sequential,
                memory=False, # <--- Memory band! No validation errors now.
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
