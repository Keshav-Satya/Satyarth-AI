import os
import streamlit as st
from crewai import Agent, LLM
from crewai.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun

# # 1. LLM Setup (SambaNova - Llama 3.3 70B)
# Sir, ye model reasoning mein best hai aur local context ko achhe se samajhta hai.
text_llm = LLM(
    model="openai/meta-llama/Llama-3.3-70B-Instruct",
    base_url="https://api.sambanova.ai/v1",
    api_key=st.secrets["SAMBANOVA_API_KEY"],
    temperature=0.1
)

# # 2. Optimized Search Tool (Token Saving Mode)
@tool('search_tool')
def search_tool(query: str):
    """Search internet for official govt, regional news, and local vendor reports."""
    search = DuckDuckGoSearchRun()
    # Sir, tokens bachane ke liye 200 characters ki limit barkarar rakhi hai.
    return search.run(query)[:200]

# # 3. Scout Agent: Local Ground Reality Scout
# Is agent ka kaam recording mein discuss kiye gaye local networks ko simulate karna hai.
scout_agent = Agent(
    role='Local Ground Reality Scout',
    goal='Global news ke bajaye local reality par focus karna aur regional entities (Vendors/Official Portals) se sachai nikaalna.',
    backstory="""Aap ek investigative journalist hain jo local networks aur vendors (jaise Verka owners/local shops) 
    ki ground reports ko analyze karte hain. Aap jaante hain ki global news asan hai, par local 1-2 websites par 
    bhari fake news ko kaise pakadna hai. Aap har fact ke saath uska source link zaroor note karte hain.""",
    tools=[search_tool],
    llm=text_llm,
    verbose=True,
    allow_delegation=False
)

# # 4. Analyst Agent: Source Transparency & Credibility Officer
# Ye agent har source ko points dega aur user ko batayega ki trust kyun karein.
analyst_agent = Agent(
    role='Source Transparency Analyst',
    goal='Har source ki credibility score calculate karna aur final report mein unhe transparently dikhana.',
    backstory="""Aap ek senior data forensic officer hain. Aap niche diye gaye formula se trust score calculate karte hain:
    - Government/Official Sources: 50% Weightage
    - Mainstream Media: 30% Weightage
    - Local Verified Reports: 15% Weightage
    - Social Media/Unknown: 5% Weightage
    
    Aap final report mein 'Sources Used' ki ek list dete hain aur batate hain ki kyun koi local news real ya fake hai.""",
    llm=text_llm,
    verbose=True,
    allow_delegation=True
)
