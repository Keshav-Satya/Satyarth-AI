import streamlit as st
import os
import time
from crewai import Agent, Task, Crew, Process
from crewai.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_google_genai import ChatGoogleGenerativeAI

# 1. Page Configuration (Zaroori pehla step)
st.set_page_config(page_title="Satyarth-AI | Digital Forensic Detective", page_icon="🕵️", layout="wide")

# 2. Cleanup & Initial Checks
os.environ["OPENAI_API_KEY"] = "NA"
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("Sir, please Dashboard mein GOOGLE_API_KEY add kijiye!")
    st.stop()

# 3. Stable Gemini Model Setup
my_llm = ChatGoogleGenerativeAI(
    model="gemini-pro", 
    google_api_key=st.secrets["GOOGLE_API_KEY"],
    temperature=0.3
)

# 4. Digital Search Tool
@tool('search_tool')
def search_tool(query: str):
    """Search the internet for news and information."""
    raw_results = DuckDuckGoSearchRun().run(query)
    return raw_results[:2000]

# --- UI Custom Styling ---
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

# --- Sidebar (Control Room) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2562/2562392.png", width=100)
    st.title("Satyarth Control Room")
    st.info("Sir, Satyarth-AI ek advanced multi-agent system hai jo news ki sachai dhoondne mein expert hai.")
    st.write("Developed with ❤️ by Team Future Flux (NIT Hamirpur)")

# --- Main Body UI ---
st.title("🕵️ Satyarth-AI")
st.subheader("Deepfake & News Verifier: The Parda-Faash Engine")

# Stylized Input Area
col1, col2 = st.columns([3, 1])
with col1:
    news_topic = st.text_input("Sir, aaj humein kis news ka 'Parda-Faash' karna hai?", placeholder="Viral news ka topic yahan likhein...")

with col2:
    st.write("##") # Vertical space
    submit_button = st.button("Satyarth Investigation Shuru Karein", type="primary")

# --- Investigation Logic ---
if submit_button:
    if news_topic:
        with st.status("🔍 Investigation Shuru...", expanded=True) as status:
            st.write("🕵️ 1. Scout Agent dimaag laga raha hai...")
            time.sleep(1) # Visual effect
            
            # Agents Definition (using existing working logic)
            scout = Agent(
                role='Digital Information Scout',
                goal=f'Verify karein ki kya "{news_topic}" news real hai ya fake.',
                backstory="Aap ek fact-checker hain jo internet se sachai nikalte hain.",
                tools=[search_tool],
                llm=my_llm,
                verbose=True
            )

            analyst = Agent(
                role='News Verifier Analyst',
                goal='Scout Agent ki report analyze karke final verdict dena.',
                backstory="Aap ek senior journalist hain jo final report taiyar karte hain.",
                llm=my_llm,
                verbose=True
            )

            # Tasks Definition
            task1 = Task(
                description=f"Internet par '{news_topic}' ke baare mein search karein aur facts collect karein.",
                agent=scout,
                expected_output="List of verified facts and sources."
            )
            task2 = Task(
                description="Saare facts ko analyze karein aur batayein ki news Real hai ya Fake.",
                agent=analyst,
                expected_output="A detailed final forensic report."
            )

            # Crew Execution
            satyarth_crew = Crew(
                agents=[scout, analyst],
                tasks=[task1, task2],
                process=Process.sequential,
                manager_llm=my_llm, # Force Gemini as Manager
                verbose=True
            )

            st.write("🔍 2. Internet se sources dhoonde ja rahe hain...")
            result = satyarth_crew.kickoff()
            status.update(label="Investigation Puri Hui! ✅", state="complete", expanded=False)

        # Final Report Display (Zabardast Card Format)
        st.markdown("### 📜 Final Forensic Report")
        st.markdown(f'<div class="report-card">{result}</div>', unsafe_allow_html=True)
        st.balloons()
    else:
        st.warning("Sir, please kuch topic toh likhiye!")
