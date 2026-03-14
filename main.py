from crewai import Crew, Process
from agents import scout_agent, analyst_agent, my_llm
from tasks import scout_task, analyst_task

# --- Satyarth Crew Setup ---
# Sir, humne agents aur tasks ko modular rakha hai
satyarth_crew = Crew(
    agents=[scout_agent, analyst_agent],
    tasks=[scout_task, analyst_task],
    process=Process.sequential, # One by one investigation
    manager_llm=my_llm,         # SambaNova ko boss (manager) banaya hai
    verbose=True
)

if __name__ == "__main__":
    print("\n--- 🕵️ Satyarth-AI System Active (NIT Hamirpur) ---")
    topic = input("Sir, kis news ki sachai verify karni hai? : ")

    if topic:
        print(f"\n🔍 Investigation Shuru: {topic}...\n")
        
        # Mission Shuru: inputs mein 'news_topic' dena zaroori hai
        # Kyunki tasks.py mein humne {news_topic} use kiya hai
        result = satyarth_crew.kickoff(inputs={'news_topic': topic})

        print("\n" + "#"*40)
        print("## 📜 FINAL INVESTIGATION REPORT ##")
        print("#"*40 + "\n")
        
        # Final result print karein
        print(result.raw)
    else:
        print("Sir, please ek valid topic enter kijiye.")
