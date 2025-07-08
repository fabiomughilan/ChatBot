# agents/summarizer_agent.py

from crewai import Agent
from llm_together import TogetherLLM  # ✅ Custom Together wrapper

# Initialize Together LLM
llm = TogetherLLM(model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo")

# Summarizer Agent
summarizer_agent = Agent(
    role="Summarizer",
    goal="Condense and summarize detailed information into clear, concise takeaways.",
    backstory=(
        "You are an expert at transforming long or complex information into short, digestible summaries. "
        "You ensure that the most important points are retained and communicated clearly."
    ),
    llm=llm,
    verbose=True  # Optional: helps with debugging
)
