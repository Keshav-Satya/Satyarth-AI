import os
import streamlit as st
from crewai import Agent, LLM
from crewai.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun

# 1. SambaNova LLM Setup - No more 404/401 Errors
# Sir, hum Llama 3.1 70B use kar rahe hain jo Gemini se fast aur stable hai
my_llm = LLM(
    model="openai/meta-llama/Llama-3.3-70B-Instruct",
    base_url="https://api.sambanova.ai/v1",
    api_key=st.secrets["SAMBANOVA_API_KEY"],
    temperature=0.1
)

# 2. Search Tool
@tool('search_tool')
def search_tool(query: str):
    """Search the internet for news, facts, and verification information."""
    search = DuckDuckGoSearchRun()
    return search.run(query)[:2000]

# 3. Scout Agent - Sachai dhundne wala detective
scout_agent = Agent(
    role='Digital Information Scout',
    goal='Viral news ki sachai verify karna aur internet se credible sources dhundna.',
    backstory="Aap ek expert digital detective hain jo fact-check karne aur afwahon ka parda-faash karne mein mahir hain.",
    tools=[search_tool],
    llm=my_llm,
    verbose=True,
    allow_delegation=False
)

# 4. Analyst Agent - Report banaye wala journalist
analyst_agent = Agent(
    role='News Verifier Analyst',
    goal='Scout Agent ki report ko analyze karke final forensic verdict dena.',
    backstory="Aap ek senior investigative journalist hain jo sources ki credibility check karke final report likhte hain.",
    llm=my_llm,
    verbose=True,
    allow_delegation=True
)

