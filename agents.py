import os
import streamlit as st
from crewai import Agent, LLM
from crewai.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun

# 1. LLM Setup (SambaNova - Llama 3.3 70B)
# Sir, hum 70B use kar rahe hain jo reasoning mein best hai
text_llm = LLM(
    model="openai/meta-llama/Llama-3.3-70B-Instruct",
    base_url="https://api.sambanova.ai/v1",
    api_key=st.secrets["SAMBANOVA_API_KEY"],
    temperature=0.1
)

# 2. Optimized Search Tool (Token Saving Mode)
@tool('search_tool')
def search_tool(query: str):
    """Search internet for official govt and regional news facts."""
    search = DuckDuckGoSearchRun()
    # Sir, humne 200 characters ki limit lagayi hai taaki rate limit na aaye
    return search.run(query)[:200]

# 3. Scout Agent: Government & Local Data Investigator
scout_agent = Agent(
    role='Lead Forensic Investigator (Official & Regional Focus)',
    goal='Verify news by strictly prioritizing Government portals (.gov, .nic, PIB) and local news sources.',
    backstory="""Aap ek digital detective hain. Aapka kaam hai sabse pehle official 
    government websites (like pib.gov.in) aur regional newspapers (like Amar Ujala, 
    Tribune) ko scan karna. Aap har fact ke saath uski website ka URL note karte hain 
    taaki use 'Source' ki tarah dikhaya ja sake.""",
    tools=[search_tool],
    llm=text_llm,
    verbose=True,
    allow_delegation=False
)

# 4. Analyst Agent: Weighted Credibility Scorer
analyst_agent = Agent(
    role='Credibility Scoring Officer',
    goal='Analyze sources and calculate a Final Satyarth Credibility Score (0-100%).',
    backstory="""Aap ek senior data analyst hain jo sources ko weightage dete hain:
    - Official Govt Sources (.gov, .nic, PIB): 50% weightage
    - Mainstream Trusted Media: 30% weightage
    - Local Verified Portals: 15% weightage
    - Social Media/Others: 5% weightage
    
    Aap final report mein ek "Credibility Score Card" aur un websites ke links 
    dete hain jinhe scan kiya gaya hai (Sources Used).""",
    llm=text_llm,
    verbose=True,
    allow_delegation=True
)
