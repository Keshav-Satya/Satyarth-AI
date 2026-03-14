from crewai import Task
from agents import scout_agent, analyst_agent

# 1. News Verification Task (Scout ke liye)
scout_task = Task(
    description=(
        "Verify karein ki kya '{news_topic}' wali news real hai ya fake? "
        "DuckDuckGo search ka use karke internet se credible sources aur latest facts ikattha karein. "
        "Check karein ki kya koi major news outlet ise report kar raha hai."
    ),
    expected_output=(
        "Ek organized list jismein verified facts, news links, aur fact-checking sources ka reference ho."
    ),
    agent=scout_agent
)

# 2. Forensic Analysis Task (Analyst ke liye)
analyst_task = Task(
    description=(
        "Scout Agent ki di hui information ko gehraai se analyze karein. "
        "Check karein ki kya news mein koi 'AI-generated' ya 'Deepfake' hone ke nishaan hain. "
        "Ek final verdict dein ki yeh news Genuine hai, Fake hai, ya Misleading."
    ),
    expected_output=(
        "Ek detailed Forensic Report jo bataye ki news asli hai ya fake aur uske piche ka solid reason kya hai."
    ),
    agent=analyst_agent
)
