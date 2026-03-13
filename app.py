import streamlit as st
import os
from crewai import Agent, Task, Crew, Process
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools import DuckDuckGoSearchRun
from crewai.tools import tool

# 1. Page Configuration
st.set_page_config(page_title="Satyarth-AI", page_icon="🕵️", layout="wide")

# 2. Block OpenAI & Verify Key
os.environ["OPENAI_API_KEY"] = "NA"
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("Sir, please Streamlit Secrets mein GOOGLE_API_KEY daaliye!")
    st.stop()

# 3. LangChain Gemini Setup (Sabse Stable Tarika)
# Sir, hum 'gemini-1.5-pro' use kar rahe hain kyunki Flash kabhi-kabhi 404 deta hai
my_llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro", 
    google_api_key=st.secrets["GOOGLE_API_KEY"],
    temperature=0.3
)

# 4. Search Tool
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
            verbose=True
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

        # Crew Configuration
        satyarth_crew = Crew(
            agents=[scout, analyst],
            tasks=[task1, task2],
            process=Process.sequential,
            manager_llm=my_llm,
            verbose=True
        )

        st.write("🔍 Sources dhoonde ja rahe hain...")
        result = satyarth_crew.kickoff()
        status.update(label="Investigation Puri Hui! ✅", state="complete")

    st.markdown("### 📜 Final Forensic Report")
    st.markdown(f'<div class="report-card">{result}</div>', unsafe_allow_html=True)
    st.balloons()
