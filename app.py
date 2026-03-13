import streamlit as st
import os
import time
from crewai import Agent, Task, Crew, Process
from crewai.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_google_genai import ChatGoogleGenerativeAI

# 1. Page Configuration (Website Layout)
st.set_page_config(page_title="Satyarth-AI | Detective", page_icon="🕵️", layout="wide")

# 2. Environment Cleanup (OpenAI ko block karna zaroori hai)
os.environ["OPENAI_API_KEY"] = "NA"

# 3. Stable Gemini Model Setup
# Sir, hum 'gemini-pro' use kar rahe hain taaki 404 error ka naam-o-nishan mit jaye
my_llm = ChatGoogleGenerativeAI(
    model="gemini-pro", 
    google_api_key=st.secrets["GOOGLE_API_KEY"],
    temperature=0.3
)

# 4. Search Tool (Internet se news dhoondne ke liye)
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
