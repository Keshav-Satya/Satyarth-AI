import streamlit as st
import os
from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun

# 1. Page Configuration
st.set_page_config(page_title="Satyarth-AI | Official", page_icon="🕵️", layout="wide")

# 2. Advanced Custom CSS for Decoration
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Forensic Report Card styling */
    .report-card {
        background-color: rgba(255, 255, 255, 0.95);
        padding: 30px;
        border-radius: 20px;
        border-top: 10px solid #FF4B4B;
        box-shadow: 0 15px 35px rgba(0,0,0,0.2);
        color: #2c3e50;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        margin-top: 20px;
    }
    
    /* Header styling */
    .main-title {
        color: #1e3799;
        font-size: 3rem !important;
        font-weight: 800;
        text-align: center;
        margin-bottom: 0px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Subtitle styling */
    .sub-title {
        text-align: center;
        color: #eb2f06;
        font-weight: 600;
        margin-bottom: 30px;
    }
    
    /* Sidebar styling */
    .stSidebar {
        background-color: #1e3799 !important;
    }
    .stSidebar .stMarkdown {
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. LLM Setup (SambaNova - Llama 3.3)
my_llm = LLM(
    model="openai/Meta-Llama-3.3-70B-Instruct", 
    base_url="https://api.sambanova.ai/v1",
    api_key=st.secrets["SAMBANOVA_API_KEY"],
    temperature=0.1
)

# 4. Search Tool
@tool('search_tool')
def search_tool(query: str):
    """Search the internet for news and facts."""
    return DuckDuckGoSearchRun().run(query)[:2000]

# --- Sidebar Content ---
with st.sidebar:
    st.markdown("# 🕵️ Satyarth-AI")
    st.markdown("### Control Center")
    st.write("---")
    st.success("✅ System: Online")
    st.info("🧠 Model: Llama-3.3-70B")
    st.write("---")
    st.markdown("🚀 **Team Future Flux**")
    st.write("NIT Hamirpur")

# --- Main UI ---
st.markdown('<h1 class="main-title">🕵️ Satyarth-AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Deepfake & News Verifier | The Truth Engine</p>', unsafe_allow_html=True)

# Input Section
with st.container():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        news_topic = st.text_input("Sir, kis news ka topic verify karna hai?", placeholder="e.g. Viral news content...")
        submit_button = st.button("Satyarth Investigation Shuru Karein", use_container_width=True, type="primary")

if submit_button and news_topic:
    with st.status("🔍 Forensic Investigation under progress...", expanded=True) as status:
        st.write("🛡️ Initializing Satyarth Agents...")
        
        scout = Agent(
            role='Digital Detective',
            goal=f'Verify facts for: {news_topic}',
            backstory="Expert fact-checker from NIT Hamirpur, specialized in digital forensics.",
            tools=[search_tool],
            llm=my_llm,
            verbose=True
        )
        
        analyst = Agent(
            role='Forensic Analyst',
            goal='Prepare a final authoritative verdict report.',
            backstory="Senior investigative journalist with a sharp eye for Deepfakes.",
            llm=my_llm,
            verbose=True
        )

        task1 = Task(description=f"Collect facts for: {news_topic}", agent=scout, expected_output="Facts and links.")
        task2 = Task(description="Prepare a professional forensic report.", agent=analyst, expected_output="Final verdict.")

        satyarth_crew = Crew(agents=[scout, analyst], tasks=[task1, task2], verbose=True)

        st.write("🌐 Scanning global databases...")
        result = satyarth_crew.kickoff()
        status.update(label="Investigation Complete! ✅", state="complete", expanded=False)

    # Final Decorated Output
    st.markdown("## 📜 Official Forensic Verdict")
    st.markdown(f"""
        <div class="report-card">
            {result.raw.replace(chr(10), '<br>')}
        </div>
    """, unsafe_allow_html=True)
    st.balloons()
