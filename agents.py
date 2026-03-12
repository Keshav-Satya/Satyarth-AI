import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from crewai.tools import BaseTool
from langchain_community.tools import DuckDuckGoSearchRun

# 1. Keys load karna
load_dotenv()

# 2. CrewAI ko batana ki hum GROQ use kar rahe hain
# Humne model name ke aage 'groq/' laga diya hai, yahi asli jaadu hai
my_llm = "groq/llama-3.1-8b-instant"

# 3. Standard Search Tool (Ismein error nahi aayega)
search_tool = DuckDuckGoSearchRun()

# 4. Scout Agent Definition
scout_agent = Agent(
    role='Digital Information Scout',
    goal='Viral news ki sachai verify karna.',
    backstory="""Aap ek digital detective hain jo internet se fact-check karte hain. 
    Aapko sirf aur sirf 'duckduckgo_search' tool ka use karna hai. 
    Kisi bhi haal mein koi aur tool (jaise brave_search) call nahi karna hai.""",
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

if __name__ == "__main__":
    # Mission (Task)
    task = Task(
        description='Verify karein ki kya "Donald Trump dancing in Indian wedding" news real hai?',
        expected_output='Ek detail report jo bataye ki news asli hai ya fake.',
        agent=scout_agent
    )

    # Team (Crew)
    satyarth_crew = Crew(
        agents=[scout_agent, analyst_agent],
        tasks=[task],
        process=Process.sequential,
        verbose=True
    )

    print("\n--- Satyarth-AI Investigation Shuru ---")
    result = satyarth_crew.kickoff()
    print("\n########################")
    print("## FINAL REPORT ##")
    print("########################\n")

    print(result)

