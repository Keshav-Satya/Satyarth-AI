from crewai import Task
from agents import scout_agent, analyst_agent

# 1. News Verification Task (Scout ke liye)
scout_task = Task(
    description='Verify karein ki kya "{news_topic}" wali news real hai ya AI generated? DuckDuckGo ka use karke sources check karein.',
    expected_output='Ek list jismein news ke links aur fact-checking sources ka reference ho.',
    agent=scout_agent
)

# 2. Deepfake Analysis Task (Analyst ke liye)
analyst_task = Task(
    description='Scout Agent ki di hui information ko analyze karein aur final verdict dein ki kya yeh news/video Deepfake hai.',
    expected_output='Ek detailed Forensic Report jo bataye ki news asli hai ya fake aur kyun.',
    agent=analyst_agent
)