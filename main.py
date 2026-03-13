from crewai import Crew, Process
from agents import scout_agent, analyst_agent, my_llm
from tasks import scout_task, analyst_task

satyarth_crew = Crew(
    agents=[scout_agent, analyst_agent],
    tasks=[scout_task, analyst_task],
    process=Process.sequential,
    manager_llm=my_llm, # <--- Yeh nayi line add karni hai (Line 10 ke paas)
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
