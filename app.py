import streamlit as st
import os
import time
from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun

# 1. Page Configuration (Website ka look)
st.set_page_config(page_title="Satyarth-AI | Detective", page_icon="🕵️", layout="wide")

# 2. Key Check
if "SAMBANOVA_API_KEY" not in st.secrets:
    st.error("Sir, please Streamlit Secrets mein SAMBANOVA_API_KEY add kijiye!")
    st.stop()

# 3. SambaNova LLM Setup (No-Error Configuration)
# Hum Llama 3.1 70B use kar rahe hain jo bohot smart aur fast hai
my_llm = LLM(
    model="openai/meta-llama/Llama-3.1-70B-Instruct", 
    base_url="https://api.sambanova.ai/v1",
    api_key=st.secrets["SAMBANOVA_API_KEY"],
    temperature=0.1
)

# 4. Search Tool Definition
@tool('search_tool')
def search_tool(query: str):
    """Internet se news aur facts scan karne ke liye search tool."""
    search = DuckDuckGoSearchRun()
    return search.run(query)[:2000]

# --- UI Styling (NIT Hamirpur Theme) ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .report-card { 
        background-color: white; 
        padding: 25px; 
        border-radius: 15px; 
        border-left: 10px solid #ff4b4b;
        box-shadow: 0px 10px 20px rgba(0,0,0,0.1);
        color: #1e1e1e;
        line-height: 1.6;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Sidebar Control Room ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2562/2562392.png", width=100)
    st.title("Satyarth Control Room")
    st.info("Sir, Satyarth-AI ab SambaNova par active hai.")
    st.write("---")
    st.write("Developed by **Team Future Flux**")

# --- Main Interface ---
st.title("🕵️ Satyarth-AI")
st.subheader("Deepfake & News Verifier: The Parda-Faash Engine")

news_topic = st.text_input("Sir, kis news ka 'Parda-Faash' karna hai?", placeholder="Viral topic yahan likhein...")
submit_button = st.button("Satyarth Investigation Shuru Karein", type="primary")

if submit_button:
    if news_topic:
        with st.status("🔍 Forensic Investigation Shuru...", expanded=True) as status:
            st.write("🕵️ Agents active ho rahe hain...")
            
            # Agent 1: Scout (Fact-Finder)
            scout = Agent(
                role='Digital Information Scout',
                goal=f'Internet se "{news_topic}" ke baare mein sahi facts dhoondna.',
                backstory="Aap ek expert digital detective hain jo internet ke kone-kone se sachai nikaalte hain.",
                tools=[search_tool],
                llm=my_llm,
                verbose=True,
                allow_delegation=False
            )

            # Agent 2: Analyst (Verdict-Giver)
            analyst = Agent(
                role='News Verifier Analyst',
                goal='Scout Agent ki report analyze karke final forensic verdict dena.',
                backstory="Aap ek senior investigative journalist hain jo fake news pehchanne mein mahir hain.",
                llm=my_llm,
                verbose=True
            )

            # Tasks
            task1 = Task(
                description=f"Internet par '{news_topic}' ke baare mein search karein aur facts collect karein.",
                agent=scout,
                expected_output="List of verified facts and credible links."
            )
            task2 = Task(
                description="Facts ko analyze karke batayein ki news Real hai ya Fake, aur reason bhi dein.",
                agent=analyst,
                expected_output="A complete forensic report with final verdict."
            )

            # Crew Execution
            satyarth_crew = Crew(
                agents=[scout, analyst],
                tasks=[task1, task2],
                process=Process.sequential,
                manager_llm=my_llm,
                memory=False, 
                verbose=True
            )

            st.write("🔍 Sources scan kiye ja rahe hain...")
            result = satyarth_crew.kickoff()
            status.update(label="Investigation Puri Hui! ✅", state="complete", expanded=False)

        # Final Report Display
        st.markdown("### 📜 Final Forensic Report")
        st.markdown(f'<div class="report-card">{result.raw}</div>', unsafe_allow_html=True)
        st.balloons()
    else:
        st.warning("Sir, please kuch topic toh likhiye!")
