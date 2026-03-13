import streamlit as st
import os
import time
from crewai import Agent, Task, Crew, Process
from crewai.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_google_genai import ChatGoogleGenerativeAI

# 1. Page Configuration (Sabse upar honi chahiye)
st.set_page_config(page_title="Satyarth-AI", page_icon="🕵️")

# 2. Cleanup
os.environ["OPENAI_API_KEY"] = "NA"

# 3. Model Check
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("Sir, please Dashboard mein GOOGLE_API_KEY add kijiye!")
    st.stop()

my_llm = ChatGoogleGenerativeAI(
    model="gemini-pro", 
    google_api_key=st.secrets["GOOGLE_API_KEY"],
    temperature=0.3
)

# 4. Tool
@tool('search_tool')
def search_tool(query: str):
    """Search the internet for news."""
    return DuckDuckGoSearchRun().run(query)[:2000]

# --- UI ---
st.title("🕵️ Satyarth-AI")
news_topic = st.text_input("News Topic:")
if st.button("Investigate"):
    with st.status("Dimaag laga raha hoon...", expanded=True):
        scout = Agent(role='Scout', goal='Find facts', backstory='Fact-checker', tools=[search_tool], llm=my_llm)
        analyst = Agent(role='Analyst', goal='Report', backstory='Journalist', llm=my_llm)
        
        task1 = Task(description=f"Verify: {news_topic}", agent=scout, expected_output="Facts")
        task2 = Task(description="Final verdict", agent=analyst, expected_output="Report")
        
        crew = Crew(agents=[scout, analyst], tasks=[task1, task2], manager_llm=my_llm)
        result = crew.kickoff()
        
    st.markdown(f"### Result\n{result}")
