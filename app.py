import streamlit as st
from main import satyarth_crew # Hamne main.py se crew ko bulaya

# Website ka Title aur Setup
st.set_page_config(page_title="Satyarth-AI", page_icon="🕵️‍♂️", layout="centered")

st.title("🕵️‍♂️ Satyarth-AI: Deepfake Verifier")
st.markdown("---")
st.write("Sir, kis news ya link ki sachai verify karni hai?")

# User Input Box
news_topic = st.text_input("Yahan news likhein:", placeholder="Example: Trump dancing in India...")

if st.button("Investigation Shuru Karein"):
    if news_topic:
        with st.spinner("Sir, agents internet par dimaag laga rahe hain..."):
            # Crew ko execute karna
            result = satyarth_crew.kickoff(inputs={'news_topic': news_topic})
            
            # Result Display
            st.success("Investigation Puri Hui!")
            st.subheader("Final Forensic Report:")
            st.markdown(result)
    else:
        st.warning("Sir, pehle kuch news toh likhiye!")