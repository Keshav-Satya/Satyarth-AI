import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from crewai.tools import tool  # <--- Yeh zaroori import hai
from langchain_community.tools import DuckDuckGoSearchRun

# 1. Keys load karna
load_dotenv()

my_llm = "groq/llama-3.1-8b-instant"

# 2. SURAKSHA KAVACH (Wrapper Tool)
# Isse Pydantic ka 'ValidationError' kabhi nahi aayega
@tool('search_tool')
def search_tool(query: str):
    """Search the internet for news and information."""
    return DuckDuckGoSearchRun().run(query)

# 3. Scout Agent Definition
scout_agent = Agent(
    role='Digital Information Scout',
    goal='Viral news ki sachai verify karna.',
    backstory="""Aap ek digital detective hain jo internet se fact-check karte hain. 
    Aapko sirf 'search_tool' ka use karna hai.""",
    tools=[search_tool],
    llm=my_llm,
    verbose=True,
    allow_delegation=False
)

# 4. Analyst Agent Definition
analyst_agent = Agent(
    role='News Verifier Analyst',
    goal='Scout Agent ki report ko analyze karke final verdict dena.',
    backstory="""Aap ek senior journalist hain jo sources ki quality check karte hain. 
    Aapka kaam Scout Agent se report lena aur uska nichod nikalna hai.""",
    llm=my_llm,
    verbose=True,
    allow_delegation=True
)
