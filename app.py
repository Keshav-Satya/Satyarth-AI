import streamlit as st
from main import satyarth_crew
import time
import requests
from streamlit_lottie import st_lottie

# 1. Page Config
st.set_page_config(page_title="Satyarth-AI | Pro Detective", page_icon="🛡️", layout="wide")

# Function for Lottie Animations
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_detective = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_at6m9vyl.json") # AI Search Animation

# 2. Advanced CSS (Cyber-Security Theme)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
    
    .stApp {
        background: linear-gradient(to right, #0f2027, #203a43, #2dbd6e20);
    }
    h1, h2, h3 {
        color: #00ffcc !important;
        font-family: 'Orbitron', sans-serif;
    }
    .report-card {
        background-color: rgba(255, 255, 255, 0.05);
        color: white;
        padding: 25px;
        border-radius: 20px;
        border: 1px solid #00ffcc;
        backdrop-filter: blur(10px);
    }
    .stButton>button {
        background: linear-gradient(45deg, #00ffcc, #0088ff);
        color: black !important;
        border: none;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0px 0px 15px #00ffcc;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar (Branding Section)
with st.sidebar:
    st.title("🛡️ Satyarth Hub")
    st.write("---")
    st_lottie(lottie_detective, height=150, key="detective")
    st.success("System: Online ✅")
    st.info("Developing a safer internet, one news at a time.")
    
    st.markdown("### 👨‍💻 Developer")
    st.write("**Keshav (NIT Hamirpur)**")
    st.write("Electrical Engineering Student")
    
    # Social Buttons
    st.markdown("[![GitHub](https://img.shields.io/badge/GitHub-Profile-lightgrey?style=for-the-badge&logo=github)](https://github.com/Keshav-Satya)")
    st.markdown("---")
    st.write("Special thanks to **Ojas Club** & **E-Cell**")

# 4. Main UI with Tabs
st.title("🕵️‍♂️ SATYARTH-AI : V2.0")
tab1, tab2, tab3 = st.tabs(["🔍 Investigation Desk", "📖 How it Works", "🎓 About"])

with tab1:
    st.markdown("### Sir, enter the news or link to verify:")
    news_input = st.text_input("", placeholder="e.g., Viral video of Prime Minister...")
    
    if st.button("RUN FORENSIC ANALYSIS"):
        if news_input:
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Simulated Processing Stages
            stages = ["Connecting to Global Servers...", "Activating Scout Agent...", "Fetching Meta-Data...", "Finalizing Cross-Verification..."]
            for i, stage in enumerate(stages):
                status_text.text(f"Processing: {stage}")
                progress_bar.progress((i + 1) * 25)
                time.sleep(1)

            # Actual AI Execution
            with st.spinner("Satyarth is generating the final report..."):
                result = satyarth_crew.kickoff(inputs={'news_topic': news_input})
                
            st.balloons()
            st.markdown("### 📜 Forensic Analysis Report")
            st.markdown(f'<div class="report-card">{result}</div>', unsafe_allow_html=True)
            
            # Option to save report
            st.download_button("Download Report as TXT", str(result), file_name="Satyarth_Report.txt")
        else:
            st.error("Sir, please provide a topic first!")

with tab2:
    st.write("### Satyarth-AI kaise kaam karta hai?")
    st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ") # Yahan aap apna demo video link dal sakte hain
    st.markdown("""
    - **Step 1:** Aap news daalte hain.
    - **Step 2:** Scout Agent poore internet ko scan karta hai.
    - **Step 3:** Analyst Agent sources ki credibility check karta hai.
    - **Step 4:** Aapko ek unbiased report milti hai.
    """)

with tab3:
    st.write("### About the Project")
    st.write("Yeh project deepfakes aur fake news ki badhti samasya ko tackle karne ke liye NIT Hamirpur mein banaya gaya hai.")
    st.image("https://www.nith.ac.in/assets/images/nith-logo.png", width=100)
