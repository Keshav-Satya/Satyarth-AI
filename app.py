import streamlit as st
import os
from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun

# 1. Page Configuration
st.set_page_config(page_title="Satyarth-AI", page_icon="🕵️", layout="wide")

# 2. Key Check
if "SAMBANOVA_API_KEY" not in st.secrets:
    st.error("Sir, please Streamlit Secrets mein SAMBANOVA_API_KEY add kijiye!")
    st.stop()

# 3. SambaNova LLM Setup - THE MASTER FIX
# Sir, 'meta-llama/' hata kar humne direct model name likha hai
my_llm = LLM(
    model="openai/Meta-Llama-3.1-70B-Instruct", 
    base_url="https://api.sambanova.ai/v1",
    api_key=st.secrets["SAMBANOVA_API_KEY"],
    temperature=0.1
)

# 4. Search Tool Setup
@tool('search_tool')
def search_tool(query: str):
    """Search the internet for news and facts."""
    search = DuckDuckGoSearchRun()
    return search.run(query)[:2000]

# --- UI Styling ---
st.markdown("""
    <style>
    .report-card { background-color: white; padding: 20px; border-radius: 15px; border-left: 8px solid #ff4b4b; color: black; box-shadow: 0px 4px 12px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

st.title("🕵️ Satyarth-AI")
st.subheader("Deepfake & News Verifier")

news_topic = st.text_input("Sir, kis news ka topic verify karna hai?", placeholder="e.g. Virat Kohli retirement...")
submit_button = st.button("Satyarth Investigation Shuru Karein", type="primary")

if submit_button and news_topic:
    with st.status("🔍 Forensic Investigation Shuru...", expanded=True) as status:
        st.write("🕵️ Agents active ho rahe hain...")
        
        # Agents
        scout = Agent(
            role='Digital Detective',
            goal=f'Verify facts for: {news_topic}',
            backstory="Expert fact-checker specialized in internet research.",
            tools=[search_tool],
            llm=my_llm,
            verbose=True
        )
        
        analyst = Agent(
            role='Forensic Analyst',
            goal='Prepare final verdict report.',
            backstory="Senior investigative journalist.",
            llm=my_llm,
            verbose=True
        )

        # Tasks
        task1 = Task(description=f"Find facts for: {news_topic}", agent=scout, expected_output="Facts list")
        task2 = Task(description="Prepare final report", agent=analyst, expected_output="Final verdict")

        # Crew Execution
        satyarth_crew = Crew(
            agents=[scout, analyst],
            tasks=[task1, task2],
            process=Process.sequential,
            verbose=True
        )

        st.write("🔍 Sachai scan ki ja rahi hai...")
        result = satyarth_crew.kickoff()
        status.update(label="Investigation Puri Hui! ✅", state="complete")

    st.markdown("### 📜 Final Forensic Report")
    st.markdown(f'<div class="report-card">{result.raw}</div>', unsafe_allow_html=True)
    st.balloons()
