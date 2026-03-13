import os
import streamlit as st
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from crewai.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_google_genai import ChatGoogleGenerativeAI # Naya Gemini Import

# 1. Keys load karna
load_dotenv()

# Yeh wala configuration ek dum stable hai
my_llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",  # <--- Flash model hi rakhein
    google_api_key=st.secrets["GOOGLE_API_KEY"], # <--- 'api_key' ko 'google_api_key' kar dein
    temperature=0.3
)

# 3. SEARCH TOOL (Stable Wrapper)
@tool('search_tool')
def search_tool(query: str):
    """Search the internet for news and information."""
    # Search results ko thoda chota rakhte hain taaki report saaf bane
    raw_results = DuckDuckGoSearchRun().run(query)
    return raw_results[:2000]

# 4. Scout Agent Definition
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

# 5. Analyst Agent Definition
analyst_agent = Agent(
    role='News Verifier Analyst',
    goal='Scout Agent ki report ko analyze karke final verdict dena.',
    backstory="""Aap ek senior journalist hain jo sources ki quality check karte hain. 
    Aapka kaam Scout Agent se report lena aur uska nichod nikalna hai.""",
    llm=my_llm,
    verbose=True,
    allow_delegation=True
)


