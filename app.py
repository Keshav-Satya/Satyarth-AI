import streamlit as st
import os
import time
from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun

# 1. Page Config
st.set_page_config(page_title="Satyarth-AI", page_icon="🕵️", layout="wide")

# 2. Permanent OpenAI Block
os.environ["OPENAI_API_KEY"] = "NA"
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("Sir, please Dashboard mein GOOGLE_API_KEY add kijiye!")
    st.stop()

# 3. Native CrewAI LLM (Is format se 404 nahi aayega)
my_llm = LLM(
    model="gemini/gemini-1.5-flash",
    api_key=st.secrets["GOOGLE_API_KEY"]
)

# 4. Tool
@tool('search_tool')
def search_tool(query: str):
    """Search the internet for news."""
    return DuckDuckGoSearchRun().run(query)[:2000]

# --- UI Styling ---
st.markdown("""
    <style>
    .report-card { background-color: white; padding: 20px; border-radius: 15px; border-left: 5px solid #ff4b4b; color: black; box-shadow: 0px 4px 12px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

st.title("🕵️ Satyarth-AI")
st.subheader("Deepfake & News Verifier")

news_topic = st.text_input("Sir, news ka topic likhein:", placeholder="e.g. Virat Kohli retirement news")
submit = st.button("Satyarth Investigation Shuru Karein", type="primary")

if submit and news_topic:
    with st.status("🔍 Investigation Shuru...", expanded=True) as status:
        # Agents
        scout = Agent(
            role='Fact-Checker',
            goal=f'Verify facts for: {news_topic}',
            backstory="Investigative detective.",
            tools=[search_tool],
            llm=my_llm,
            verbose=True
        )
        analyst = Agent(
            role='Journalist',
            goal='Final verdict dena.',
            backstory="Senior editor.",
            llm=my_llm,
            verbose=True
        )

        # Tasks
        t1 = Task(description=f"Search facts: {news_topic}", agent=scout, expected_output="Facts list")
        t2 = Task(description="Prepare final report", agent=analyst, expected_output="Final Report")

        # --- THE PERMANENT FIX ---
        satyarth_crew = Crew(
            agents=[scout, analyst],
            tasks=[t1, t2],
            process=Process.sequential,
            manager_llm=my_llm, # Manager ko Gemini diya
            embedder={          # Embedder ko bhi Gemini par force kiya
                "provider": "google",
                "config": {"model": "models/text-embedding-004", "api_key": st.secrets["GOOGLE_API_KEY"]}
            },
            verbose=True
        )

        result = satyarth_crew.kickoff()
        status.update(label="Investigation Puri Hui! ✅", state="complete")

    st.markdown("### 📜 Final Forensic Report")
    st.markdown(f'<div class="report-card">{result.raw}</div>', unsafe_allow_html=True)
    st.balloons()
