from crewai import Crew, Process
from agents import scout_agent, analyst_agent
from tasks import scout_task, analyst_task

# Satyarth-AI ki Team (Crew) banana
satyarth_crew = Crew(
    agents=[scout_agent, analyst_agent],
    tasks=[scout_task, analyst_task],
    process=Process.sequential, # Pehle Scout, phir Analyst
    verbose=True
)

if __name__ == "__main__":
    print("--- Satyarth-AI System Active ---")
    topic = input("Sir, kis news ki sachai verify karni hai? : ")
    
    # Mission Shuru
    result = satyarth_crew.kickoff(inputs={'news_topic': topic})
    
    print("\n########################")
    print("## FINAL INVESTIGATION REPORT ##")
    print("########################\n")
    print(result)