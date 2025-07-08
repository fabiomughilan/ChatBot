# 🧠 HealthMind AI - Fabio Mughilan

![ChatBot UI Screenshot](https://github.com/user-attachments/assets/bf43935d-4326-4a9a-bbf5-ed1784235a5a)

🚀 [Launch Live ChatBot](https://fabiomughilan-chatbot-chat-agentschat-ui-cdgxwc.streamlit.app/)

**HealthMind AI** is a smart and compassionate AI chatbot that provides personalized support in the domains of **mental health** and **dietary advice**. Powered by multi-agent architecture using `CrewAI`, it leverages large language models (LLMs) via `Together.ai`, along with semantic search using `ChromaDB`.

---

## 📖 Features

- 🔍 **Topic Classification** — Routes user queries to either the *Mental Health* or *Diet* agent using a supervisor agent.
- 🧠 **Expert Agents** — Specialized agents for Mental Health and Diet, each with context-aware expertise.
- 📚 **Semantic Knowledge Retrieval** — Queries are matched against a curated local knowledge base using vector embeddings (via Sentence Transformers).
- ✨ **Summarizer Agent** — Cleans and shortens lengthy responses into clear, actionable takeaways.
- 🌐 **FastAPI Backend** — Handles agent orchestration and response pipeline.
- 🧑‍💻 **Streamlit UI** — Lightweight web-based interface for users to chat easily.

---

## ⚙️ Tools & Technologies

| Technology | Usage |
|------------|--------|
| 🧠 **CrewAI** | Multi-agent orchestration |
| 💬 **Together.ai API** | LLM backend (Mixtral-8x7B via Together) |
| 🧾 **FastAPI** | Backend API for agent routing and responses |
| 📚 **ChromaDB** | Persistent vector store for semantic retrieval |
| 🧪 **SentenceTransformer** | BAAI/bge-small-en-v1.5 for text embedding |
| 🧑‍💻 **Streamlit** | Frontend interface for chatbot |
| 🌱 **Python-dotenv** | Securely handle API keys and config |
| 📄 **LangChain-style LLM Tooling** | Via CrewAI + LiteLLM abstraction |

---

## 🛠 Installation & Setup

> 💡 **Note:** Python 3.10+ is recommended.

### 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/chat-agents.git
cd chat-agents
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
TOGETHER_API_KEY=your_together_ai_api_key_here
uvicorn bot:app --reload
cd chat-ui
streamlit run ui.py

agents/
├── supervisor_agent.py      # Classifies queries into topics
├── diet_agent.py            # Handles diet & nutrition queries
├── mental_health_agent.py   # Responds to emotional wellness queries
└── summarizer_agent.py      # Shortens and polishes final output

vector_db.py                 # Knowledge base management using ChromaDB
bot.py                       # Core FastAPI orchestration


