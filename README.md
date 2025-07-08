
# 🧠 HealthMind AI - Fabio Mughilan

![ChatBot UI Screenshot](https://github.com/user-attachments/assets/bf43935d-4326-4a9a-bbf5-ed1784235a5a)

🚀 [Launch Live ChatBot](https://fabiomughilan-chatbot-chat-agentschat-ui-cdgxwc.streamlit.app/)

**HealthMind AI** is a smart and compassionate AI chatbot that provides personalized support in the domains of **mental health** and **dietary advice**. Powered by a multi-agent architecture using `CrewAI`, it leverages large language models (LLMs) via `Together.ai`, along with semantic search using `ChromaDB`.
Tech Stack - Python, Flask
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

| Technology           | Purpose                                       |
|----------------------|-----------------------------------------------|
| 🧠 CrewAI             | Multi-agent orchestration                     |
| 💬 Together.ai API   | LLM backend (Mixtral-8x7B model)              |
| 🧾 FastAPI            | Backend API for query handling                |
| 📚 ChromaDB           | Vector store for knowledge retrieval          |
| 🧪 SentenceTransformer| Embedding queries (`BAAI/bge-small-en-v1.5`)  |
| 📺 Streamlit          | Frontend UI for chat                          |
| 🌱 Python-dotenv      | Environment variable handling                 |

---

## 🛠 Installation & Setup

> 💡 **Note:** Python 3.10+ is recommended.

### 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/chat-agents.git
cd chat-agents
```

### 2. Set up Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Add Environment Variables

Create a `.env` file in the root directory with your Together.ai API key:

```env
TOGETHER_API_KEY=your_together_ai_api_key_here
```

### 5. Run the Backend (FastAPI)

```bash
uvicorn bot:app --reload
```

Backend runs at: `http://127.0.0.1:8000`

### 6. Run the Frontend (Streamlit)

```bash
cd chat-ui
streamlit run ui.py
```

---

## 🗂 Project Structure

```
.
├── agents/
│   ├── supervisor_agent.py       # Classifies query into topics
│   ├── diet_agent.py             # Handles dietary queries
│   ├── mental_health_agent.py    # Handles mental health queries
│   └── summarizer_agent.py       # Shortens long responses
│
├── vector_db.py                  # ChromaDB + embeddings logic
├── bot.py                        # FastAPI orchestration logic
├── chat-ui/
│   └── ui.py                     # Streamlit frontend
├── requirements.txt
└── .env                          # Environment file (not committed)
```

---

## 📌 Example Queries

- "I'm feeling anxious all the time, what can I do?"
- "What is a good vegetarian snack for muscle gain?"
- "How can I practice mindfulness daily?"

---

## 📈 Future Enhancements

- 🛡 Add user login & history
- 🌍 Multilingual LLM support
- 🧾 Editable admin KB interface
- 📊 Query analytics dashboard

---

## 🤝 Contributing

Pull requests and feedback are welcome!  
To contribute:

1. Fork this repo  
2. Create a new branch (`git checkout -b feature/your-feature`)  
3. Commit your changes (`git commit -m "feat: add your feature"`)  
4. Push to the branch (`git push origin feature/your-feature`)  
5. Open a Pull Request

---

## 📜 License

This project is licensed under the **MIT License**.

---

## 👤 Author

**T. Fabio Mughilan**  
🔗 [LinkedIn](https://www.linkedin.com/in/fabiomughilan)  
📫 Email: fabiomughilan@gmail.com
