import streamlit as st
import os
import time
from crewai import Agent, Task, Crew, Process, LLM # <--- Naya LLM import
from crewai.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun

# 1. Page Configuration
st.set_page_config(page_title="Satyarth-AI | Detective", page_icon="🕵️", layout="wide")

# 2. BOHOT ZAROORI: OpenAI ko poori tarah block karna
os.environ["OPENAI_API_KEY"] = "" # Ise khali chhod dein
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("Sir, please Dashboard mein GOOGLE_API_KEY add kijiye!")
    st.stop()

# 3. CrewAI Native Gemini Setup (Sabse Stable Tarika)
# Hum 'gemini/' prefix use karenge taaki CrewAI ko pata chale ki kahan jana hai
my_llm = LLM(
    model="gemini/gemini-1.5-flash", 
    api_key=st.secrets["GOOGLE_API_KEY"]
)

# 4. Search Tool
@tool('search_tool')
def search_tool(query: str):
    """Search the internet for news and information."""
    return DuckDuckGoSearchRun().run(query)[:2000]

# --- UI Styling ---
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .report-card { 
        background-color: white; 
        padding: 20px; 
        border-radius: 15px; 
        border-left: 5px solid #ff4b4b;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2562/2562392.png", width=100)
    st.title("Satyarth Control Room")
    st.info("Sir, Satyarth-AI multi-agent system ab active hai.")
    st.write("Developed with ❤️ by Team Future Flux")

# --- Main UI ---
st.title("🕵️ Satyarth-AI")
st.subheader("Deepfake & News Verifier: The Parda-Faash Engine")

news_topic = st.text_input("Sir, aaj humein kis news ka 'Parda-Faash' karna hai?", placeholder="Viral news topic...")
submit_button = st.button("Satyarth Investigation Shuru Karein", type="primary")

if submit_button:
    if news_topic:
        with st.status("🔍 Investigation Shuru...", expanded=True) as status:
            st.write("🕵️ 1. Agents charge up ho rahe hain...")
            
            # Agents Definition with Native LLM
            scout = Agent(
                role='Digital Information Scout',
                goal=f'Verify karein: {news_topic}',
                backstory="Fact-checker detective.",
                tools=[search_tool],
                llm=my_llm, # Native Gemini
                verbose=True,
                allow_delegation=False
            )

            analyst = Agent(
                role='News Verifier Analyst',
                goal='Analyze facts and give final verdict.',
                backstory="Senior investigative journalist.",
                llm=my_llm, # Native Gemini
                verbose=True
            )

            # Tasks
            task1 = Task(description=f"Search facts about: {news_topic}", agent=scout, expected_output="Facts list")
            task2 = Task(description="Prepare final forensic report", agent=analyst, expected_output="Final Report")

            # Crew Execution (Explicitly disabling OpenAI Embeddings)
            satyarth_crew = Crew(
                agents=[scout, analyst],
                tasks=[task1, task2],
                process=Process.sequential,
                # ZAROORI: Embedder ko bhi Gemini par set kar rahe hain
                embedder={
                    "provider": "google",
                    "config": {"model": "models/embedding-001", "api_key": st.secrets["GOOGLE_API_KEY"]}
                },
                verbose=True
            )

            st.write("🔍 2. Internet se sachai nikaali ja rahi hai...")
            result = satyarth_crew.kickoff()
            status.update(label="Investigation Puri Hui! ✅", state="complete", expanded=False)

        st.markdown("### 📜 Final Forensic Report")
        st.markdown(f'<div class="report-card">{result.raw}</div>', unsafe_allow_html=True)
        st.balloons()
    else:
        st.warning("Sir, please kuch topic likhiye!")
