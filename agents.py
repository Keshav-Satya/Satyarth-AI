import os
import streamlit as st
from crewai import Agent, Task, Crew, Process
from crewai.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_google_genai import ChatGoogleGenerativeAI

# 1. Environment variables set karna (CrewAI ke liye)
os.environ["OPENAI_API_KEY"] = "NA"
os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]

# 2. Gemini Model (Ek dum stable configuration)
# Note: Hum 'gemini-1.5-flash' use karenge jo sabse fast hai
my_llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash", 
    google_api_key=st.secrets["GOOGLE_API_KEY"],
    temperature=0.3
)

# 3. SEARCH TOOL
@tool('search_tool')
def search_tool(query: str):
    """Search the internet for news and information."""
    raw_results = DuckDuckGoSearchRun().run(query)
    return raw_results[:2000]

# 4. Scout Agent (LLM parameter pakka check karein)
scout_agent = Agent(
    role='Digital Information Scout',
    goal='Viral news ki sachai verify karna.',
    backstory="Aap ek digital detective hain jo internet se fact-check karte hain.",
    tools=[search_tool],
    llm=my_llm, # <--- YEH SABSE ZAROORI HAI SIR
    verbose=True,
    allow_delegation=False
)

# 5. Analyst Agent (LLM parameter pakka check karein)
analyst_agent = Agent(
    role='News Verifier Analyst',
    goal='Scout Agent ki report ko analyze karke final verdict dena.',
    backstory="Aap ek senior journalist hain jo sources ki credibility check karte hain.",
    llm=my_llm, # <--- YEH BHI ZAROORI HAI SIR
    verbose=True,
    allow_delegation=True
)

