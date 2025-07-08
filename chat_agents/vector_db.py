import os
import logging
from typing import List
from dotenv import load_dotenv
import chromadb
from sentence_transformers import SentenceTransformer

# Load environment variables
load_dotenv()

# Setup Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Load Embedding Model
model = SentenceTransformer("BAAI/bge-small-en-v1.5")

class LocalEmbeddingFunction:
    def __call__(self, input: List[str]) -> List[List[float]]:
        if isinstance(input, str):
            input = [input]
        return model.encode(input, convert_to_numpy=True).tolist()

    def name(self):
        return "bge-small-en-v1.5"

# Initialize ChromaDB
DB_PATH = "./vector_db"
chroma_client = chromadb.PersistentClient(path=DB_PATH)
embedding_function = LocalEmbeddingFunction()

mental_health_collection = chroma_client.get_or_create_collection(
    name="mental_health_knowledge",
    embedding_function=embedding_function
)

diet_collection = chroma_client.get_or_create_collection(
    name="diet_knowledge",
    embedding_function=embedding_function
)

# --- KNOWLEDGE BASES ---
MENTAL_HEALTH_KB = {
    "stress relief": "Practice deep breathing, progressive muscle relaxation, and take regular breaks from screens and work.",
    "anxiety management": "Try grounding techniques like 5-4-3-2-1, journaling, and talking to someone you trust.",
    "burnout symptoms": "Burnout may include emotional exhaustion, lack of motivation, irritability, and trouble sleeping.",
    "self-compassion": "Be kind to yourself. Self-compassion involves accepting mistakes, being mindful, and avoiding harsh criticism.",
    "mindfulness": "Mindfulness involves paying attention to the present moment without judgment. Meditation can help build mindfulness.",
}

DIET_KB = {
    "balanced diet": "A balanced diet includes fruits, vegetables, whole grains, lean protein, and healthy fats in the right proportions.",
    "hydration": "Drink at least 8 glasses of water daily. Proper hydration aids digestion and improves concentration.",
    "weight loss tips": "Focus on portion control, avoid processed foods, exercise regularly, and stay consistent with habits.",
    "intermittent fasting": "Intermittent fasting involves eating within a time-restricted window (e.g., 16:8). It may help manage weight.",
    "healthy snacks": "Opt for nuts, fruits, yogurt, or boiled eggs instead of sugary snacks to maintain energy and avoid crashes.",
}

# --- Embedding ---
def get_embedding(text: str) -> List[float] | None:
    if not text or not isinstance(text, str):
        return None
    try:
        return model.encode([text], convert_to_numpy=True)[0].tolist()
    except Exception as e:
        logger.error(f"Embedding error: {str(e)}")
        return None

# --- Insert into DB ---
def insert_knowledge():
    logger.info("📚 Indexing Mental Health Knowledge...")
    existing_ids = set(mental_health_collection.get(ids=None)["ids"])
    for k, v in MENTAL_HEALTH_KB.items():
        if k not in existing_ids:
            emb = get_embedding(v)
            if emb:
                mental_health_collection.add(ids=[k], embeddings=[emb], metadatas=[{"text": v}])

    logger.info("🍎 Indexing Diet Knowledge...")
    existing_ids = set(diet_collection.get(ids=None)["ids"])
    for k, v in DIET_KB.items():
        if k not in existing_ids:
            emb = get_embedding(v)
            if emb:
                diet_collection.add(ids=[k], embeddings=[emb], metadatas=[{"text": v}])

# --- Query ---
def query_knowledge(query: str, topic: str) -> str:
    emb = get_embedding(query)
    if emb is None:
        return "Unable to process your query."

    if topic == "mental health":
        collection = mental_health_collection
    elif topic == "diet":
        collection = diet_collection
    else:
        return "Topic not supported."

    results = collection.query(query_embeddings=[emb], n_results=3)

    matches = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    if not matches:
        return "No relevant answer found."

    # Filter and combine based on distance threshold
    threshold = 0.5
    responses = [
        match["text"] for i, match in enumerate(matches) if distances[i] < threshold
    ]

    return "\n\n".join(responses) if responses else "No strong match found."

# --- Auto-index knowledge on import ---
insert_knowledge()
logger.info("✅ Knowledge bases loaded and indexed.")
