# mental_health_agent.py
from crewai import Agent
from dotenv import load_dotenv
import os
from llm_together import TogetherLLM  # ✅ use direct SDK wrapper

# Load environment variables
load_dotenv()

# Initialize Together LLM
llm = TogetherLLM(model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo")

# Mental Health Expert Agent
mental_health_agent = Agent(
    role="Mental Health Advisor",
    goal="Provide compassionate, evidence-based mental health support.",
    backstory="You are a mental health expert focused on emotional well-being, stress, anxiety, and self-care strategies.",
    llm=llm,
    verbose=True  # Optional for debugging output
)
