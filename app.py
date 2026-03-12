import streamlit as st
from main import satyarth_crew
import time

# 1. Page Configuration (Website ka tab aur layout)
st.set_page_config(
    page_title="Satyarth-AI | Deepfake Detective",
    page_icon="🕵️‍♂️",
    layout="wide"
)

# 2. Custom CSS for Styling (Website ko 'Pyara' banane ka jaadu)
st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
    }
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        height: 3em;
        background-color: #ff4b4b;
        color: white;
        font-weight: bold;
        border: none;
    }
    .stTextInput>div>div>input {
        border-radius: 15px;
    }
    .report-card {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
        border-left: 5px solid #ff4b4b;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar (Information aur Settings ke liye)
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2562/2562392.png", width=100) # Ek cool detective icon
    st.title("Satyarth Control Room")
    st.info("Sir, Satyarth-AI ek advanced multi-agent system hai jo news ki sachai dhoondne mein expert hai.")
    st.markdown("---")
    st.write("🔧 **System Settings**")
    model_speed = st.select_slider("Analysis Depth", options=["Quick", "Standard", "Deep"])
    st.write("Developed with ❤️ by **Team Future Flux (NIT Hamirpur)**")

# 4. Main Body UI
col1, col2 = st.columns([1, 2]) # Screen ko do parts mein baanta

with col1:
    # Yahan hum koi animation ya image dikha sakte hain
    st.title("🕵️‍♂️")
    st.header("Satyarth-AI")
    st.subheader("Deepfake & News Verifier")

with col2:
    st.write("---")
    st.markdown("### Sir, aaj humein kis news ka 'Parda-Faash' karna hai?")
    news_topic = st.text_input("", placeholder="Yahan news ka topic ya link likhein...")
    
    submit_button = st.button("Satyarth Investigation Shuru Karein")

# 5. Result Section
if submit_button:
    if news_topic:
        with st.status("🔍 Investigation Shuru...", expanded=True) as status:
            st.write("1. Scout Agent dimaag laga raha hai...")
            time.sleep(1)
            st.write("2. Internet se sources dhoonde ja rahe hain...")
            
            # Crew Execution
            result = satyarth_crew.kickoff(inputs={'news_topic': news_topic})
            
            status.update(label="Investigation Puri Hui! ✅", state="complete", expanded=False)

        st.markdown("### 📜 Final Forensic Report")
        st.markdown(f'<div class="report-card">{result}</div>', unsafe_allow_html=True)
        
        # Ek pyara sa celebration effect
        st.balloons()
    else:
        st.warning("Sir, bina news ke detective kya dhoondega? Please kuch topic likhiye.")
