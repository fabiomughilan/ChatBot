# /agents/diet_agent.py

from crewai import Agent, Task, Crew
from dotenv import load_dotenv
import os

from llm_together import TogetherLLM

load_dotenv()

# Use Together's LLM wrapper instead of litellm
llm = TogetherLLM(model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo")

# Diet Agent
diet_agent = Agent(
    role="Dietician",
    goal="Provide personalized diet guidance and nutrition tips.",
    backstory="You are a certified nutritionist and diet expert focused on healthy, balanced diets tailored to individuals' needs. Your responses are rooted in up-to-date dietary science and lifestyle adaptation.",
    llm=llm,
    verbose=True  # Optional: helpful for debugging
)

# Diet Task
diet_task = Task(
    description=(
        "You are assisting a user who has asked a question related to diet or nutrition.\n"
        "- Use evidence-based nutrition knowledge.\n"
        "- Tailor advice for common goals like weight loss, muscle gain, balanced eating, etc.\n"
        "- Consider dietary restrictions if mentioned (e.g., vegetarian, gluten-free).\n"
        "- Be positive, actionable, and concise.\n\n"
        "User query: {query}"
    ),
    agent=diet_agent,
    expected_output="A personalized diet or nutrition recommendation based on the query."
)

# Function to run the crew for diet-related queries
def handle_diet_query(query: str) -> str:
    crew = Crew(
        agents=[diet_agent],
        tasks=[diet_task]
    )
    output = crew.kickoff(inputs={"query": query})
    return str(output).strip()
