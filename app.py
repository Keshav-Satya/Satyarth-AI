import streamlit as st
import os
import time
from crewai import Agent, Task, Crew, Process
from crewai.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_google_genai import ChatGoogleGenerativeAI

# 1. Page Configuration
st.set_page_config(page_title="Satyarth-AI | Detective", page_icon="🕵️", layout="wide")

# 2. Force environment variables (SABSE ZAROORI)
os.environ["OPENAI_API_KEY"] = "NA" 
# Is line ko mita dein:
os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]

# 3. Gemini Model Define karna
my_llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=st.secrets["GOOGLE_API_KEY"],
    temperature=0.3
)

# 4. Search Tool
@tool('search_tool')
def search_tool(query: str):
    """Search the internet for news and information."""
    raw_results = DuckDuckGoSearchRun().run(query)
    return raw_results[:2000]

# --- UI Layout ---
st.title("🕵️ Satyarth-AI")
st.subheader("Deepfake & News Verifier")

news_topic = st.text_input("Sir, aaj humein kis news ka 'Parda-Faash' karna hai?", placeholder="Yahan news topic likhein...")
submit_button = st.button("Satyarth Investigation Shuru Karein")

if submit_button:
    if news_topic:
        with st.status("🔍 Investigation Shuru...", expanded=True) as status:
            # Agents fresh define kar rahe hain taaki OpenAI call na ho
            scout = Agent(
                role='Digital Information Scout',
                goal='Viral news ki sachai verify karna.',
                backstory="Aap ek fact-checker hain.",
                tools=[search_tool],
                llm=my_llm,
                verbose=True
            )

            analyst = Agent(
                role='News Verifier Analyst',
                goal='Final verdict dena.',
                backstory="Aap ek senior journalist hain.",
                llm=my_llm,
                verbose=True
            )

            # Tasks fresh define kar rahe hain (Adding LLM here too!)
            task1 = Task(description=f"Verify news: {news_topic}", agent=scout, expected_output="Facts list")
            task2 = Task(description="Analyze facts and give final verdict", agent=analyst, expected_output="Final Report")

            # Crew Setup
            satyarth_crew = Crew(
                agents=[scout, analyst],
                tasks=[task1, task2],
                process=Process.sequential,
                manager_llm=my_llm, # Force Gemini as Manager
                verbose=True
            )

            st.write("🕵️ Agents dimaag laga rahe hain...")
            result = satyarth_crew.kickoff()
            status.update(label="Investigation Puri Hui! ✅", state="complete", expanded=False)

        st.markdown("### 📜 Final Forensic Report")
        st.write(result.raw)
        st.balloons()
    else:
        st.warning("Sir, please topic likhiye.")

