import os
import streamlit as st
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from crewai.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_google_genai import ChatGoogleGenerativeAI # Naya Gemini Import

# 1. Keys load karna
load_dotenv()

os.environ["OPENAI_API_KEY"] = "NA"
# Yeh configuration sabse zyada stable hai aur 404 error ko khatam kar degi
my_llm = ChatGoogleGenerativeAI(
    model="gemini-pro", # <--- Ise 'gemini-pro' kar dein, yeh sabse reliable hai
    google_api_key=st.secrets["GOOGLE_API_KEY"], 
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
    backstory="Aap ek fact-checker hain.",
    tools=[search_tool],
    verbose=True,
    allow_delegation=False,
    llm=my_llm  # <--- YEH LINE HONA BOHOT ZAROORI HAI!
)

# 5. Analyst Agent Definition
analyst_agent = Agent(
    role='News Verifier Analyst',
    goal='Report analyze karke final verdict dena.',
    backstory="Aap ek senior journalist hain.",
    verbose=True,
    allow_delegation=True,
    llm=my_llm  # <--- YEH BHI ZAROORI HAI!
)






