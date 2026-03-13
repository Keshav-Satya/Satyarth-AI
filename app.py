import streamlit as st
import os
from crewai import Agent, Task, Crew, Process
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools import DuckDuckGoSearchRun
from crewai.tools import tool

# 1. Page Configuration
st.set_page_config(page_title="Satyarth-AI", page_icon="🕵️", layout="wide")

# 2. Block OpenAI (Force Gemini)
os.environ["OPENAI_API_KEY"] = "NA"

# 3. Stable Gemini Setup
# Sir, 'gemini-pro' sabse stable model hai jo 404 error nahi deta.
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("Sir, please Streamlit Secrets mein GOOGLE_API_KEY add kijiye!")
    st.stop()

my_llm = ChatGoogleGenerativeAI(
    model="gemini-pro", 
    google_api_key=st.secrets["GOOGLE_API_KEY"],
    temperature=0.3
)

# 4. Search Tool Setup
@tool('search_tool')
def search_tool(query: str):
    """Search the internet for news and information."""
    search = DuckDuckGoSearchRun()
    return search.run(query)[:2000]

# --- UI Layout ---
st.markdown("""
    <style>
    .report-card { background-color: white; padding: 20px; border-radius: 15px; border-left: 5px solid #ff4b4b; color: black; }
    </style>
    """, unsafe_allow_html=True)

st.title("🕵️ Satyarth-AI")
st.subheader("Deepfake & News Verifier")

news_topic = st.text_input("Sir, kis news ka 'Parda-Faash' karna hai?", placeholder="Viral topic yahan likhein...")
submit_button = st.button("Satyarth Investigation Shuru Karein", type="primary")

if submit_button and news_topic:
    with st.status("🔍 Investigation Shuru...", expanded=True) as status:
        st.write("🕵️ Agents active ho rahe hain...")
        
        # Agents
        scout = Agent(
            role='Digital Detective',
            goal=f'Verify facts for: {news_topic}',
            backstory="Aap ek expert fact-checker hain.",
            tools=[search_tool],
            llm=my_llm,
            verbose=True
        )
        
        analyst = Agent(
            role='Forensic Analyst',
            goal='Prepare a final report.',
            backstory="Aap ek senior investigative journalist hain.",
            llm=my_llm,
            verbose=True
        )

        # Tasks
        task1 = Task(description=f"Find facts for: {news_topic}", agent=scout, expected_output="List of facts")
        task2 = Task(description="Prepare final verdict", agent=analyst, expected_output="Final report")

        # Crew - Sabse Stable Configuration
        satyarth_crew = Crew(
            agents=[scout, analyst],
            tasks=[task1, task2],
            process=Process.sequential,
            verbose=True
        )

        st.write("🔍 Sachai dhoondi ja rahi hai...")
        result = satyarth_crew.kickoff()
        status.update(label="Investigation Puri Hui! ✅", state="complete")

    st.markdown("### 📜 Final Forensic Report")
    st.markdown(f'<div class="report-card">{result}</div>', unsafe_allow_html=True)
    st.balloons()
