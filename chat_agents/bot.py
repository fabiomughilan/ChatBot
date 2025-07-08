import logging
import os
import asyncio
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv

from crewai import Task, Crew

# Load environment variables
load_dotenv()

# Initialize logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(title="HealthMind AI", version="1.0")
app.state.recent_queries = {}

# Request model
class QueryRequest(BaseModel):
    query: str
    session_id: str = "default_session"

# Import agents
from agents.supervisor_agent import supervisor_agent
from agents.mental_health_agent import mental_health_agent
from agents.diet_agent import diet_agent
from agents.summarizer_agent import summarizer_agent

# Import vector DB
import vector_db

# --- Task Generators ---
def create_topic_task(agent, topic, context):
    return Task(
        description=(
            f"Use the knowledge below to answer the user's query related to {topic}:\n\n"
            f"Query: {{query}}\n\nKnowledge:\n{context}"
        ),
        agent=agent,
        expected_output="Helpful expert-level answer"
    )

supervisor_task = Task(
    description="Classify the topic of the user query as either 'mental health' or 'diet'.\n"
                "Return only the topic label.\n\nQuery: {query}",
    agent=supervisor_agent,
    expected_output="One of: mental health or diet"
)

summarizer_task = Task(
    description="Summarize the response into a short, user-friendly answer without losing key information.\n\nResponse: {raw_response}",
    agent=summarizer_agent,
    expected_output="Clean, structured summary"
)

# --- Main Endpoint ---
@app.post("/query")
async def handle_query(request: QueryRequest):
    logger.info(f"🔍 Received query: {request.query}")
    session_id = request.session_id
    app.state.recent_queries.setdefault(session_id, []).append(request.query)
    app.state.recent_queries[session_id] = app.state.recent_queries[session_id][-5:]

    # Step 1: Classify topic
    try:
        supervisor_crew = Crew(agents=[supervisor_agent], tasks=[supervisor_task])
        topic_result = await asyncio.to_thread(supervisor_crew.kickoff, inputs={"query": request.query})
        topic = str(topic_result).strip().lower()
        logger.info(f"🧠 Topic classified: {topic}")
    except Exception as e:
        logger.error(f"🚨 Supervisor classification failed: {e}")
        return {"response": "Error identifying topic. Please try again."}

    if topic not in ["mental health", "diet"]:
        return {"response": "Sorry, I couldn't understand the topic. Please ask about mental health or diet."}

    # Step 2: Retrieve domain-specific knowledge
    knowledge = vector_db.query_knowledge(request.query, topic)
    if "no relevant" in knowledge.lower():
        return {"response": "I couldn't find information on that. Could you rephrase or try a different query?"}

    # Step 3: Run domain-specific agent
    try:
        selected_agent = mental_health_agent if topic == "mental health" else diet_agent
        topic_task = create_topic_task(selected_agent, topic, context=knowledge)
        topic_crew = Crew(agents=[selected_agent], tasks=[topic_task])
        raw_response = await asyncio.to_thread(topic_crew.kickoff, inputs={"query": request.query})
    except Exception as e:
        logger.error(f"🚨 Agent response failed: {e}")
        return {"response": "There was an issue generating a response. Please try again shortly."}

    # Step 4: Summarize final output
    try:
        summarizer_crew = Crew(agents=[summarizer_agent], tasks=[summarizer_task])
        final_response = await asyncio.to_thread(summarizer_crew.kickoff, inputs={"raw_response": str(raw_response)})
    except Exception as e:
        logger.error(f"🚨 Summarization failed: {e}")
        return {"response": str(raw_response)}  # fallback to raw if summarization fails

    logger.info("✅ Response ready")
    return {"response": str(final_response).strip()}
