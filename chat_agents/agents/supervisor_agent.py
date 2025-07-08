# agents/supervisor_agent.py

from crewai import Agent
from llm_together import TogetherLLM  # ✅ use direct SDK wrapper import TogetherLLM

# Initialize Together LLM (e.g., Meta-Llama or Mistral)
llm = TogetherLLM(model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo")

# Define the Supervisor Agent
supervisor_agent = Agent(
    role="Topic Classification Expert",
    goal="Understand user queries and classify them correctly into health domains.",
    backstory=(
        "You are an expert classifier that understands health-related user queries "
        "and can route them to either the mental health agent or the diet agent. "
        "You never guess — only return the most relevant category."
    ),
    llm=llm
)
