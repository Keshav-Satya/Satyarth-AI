import os
import streamlit as st
from crewai import Agent, Task, Crew, Process
from crewai.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_google_genai import ChatGoogleGenerativeAI

# 1. Sabse zaroori: Purani yaadein mitao
# Sir, check kijiye ki yahan GOOGLE_API_KEY wala koi os.environ na ho!
os.environ["OPENAI_API_KEY"] = "NA"

# Yeh configuration sabse zyada stable hai aur 404 error ko khatam kar degi
my_llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash", 
    google_api_key=st.secrets["GOOGLE_API_KEY"], # <--- 'api_key' ko 'google_api_key' kar dein
    temperature=0.3
)

# 3. SEARCH TOOL
@tool('search_tool')
def search_tool(query: str):
    """Search the internet for news and information."""
    raw_results = DuckDuckGoSearchRun().run(query)
    return raw_results[:2000]

# 4. Scout Agent
scout_agent = Agent(
    role='Digital Information Scout',
    goal='Viral news ki sachai verify karna.',
    backstory="Aap ek digital detective hain jo fact-check karte hain.",
    tools=[search_tool],
    llm=my_llm, # <--- Sir, yeh line Gemini se connect karti hai
    verbose=True,
    allow_delegation=False
)

# 5. Analyst Agent
analyst_agent = Agent(
    role='News Verifier Analyst',
    goal='Scout Agent ki report ko analyze karke final verdict dena.',
    backstory="Aap ek senior journalist hain jo sources ki credibility check karte hain.",
    llm=my_llm, # <--- Yeh line bhi Gemini use karegi
    verbose=True,
    allow_delegation=True
)

