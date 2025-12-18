# AI Customer Support Bot
This project is a full-stack AI support agent designed to automate customer service using a Retrieval-Augmented Generation (RAG) architecture. It integrates a FastAPI backend with a Streamlit frontend, utilizing Ollama to run Large Language Models locally.

# Features
* Local AI Processing: Uses Ollama for private, local LLM execution (Llama3).

* Contextual Memory: Tracks user sessions and chat history via a persistent SQLite database.

* FAQ Retrieval: Uses ChromaDB as a vector store to find relevant answers from a 100+ FAQ dataset.

* Automatic Escalation: Detects when a query cannot be answered and suggests human intervention.

* Session Tracking: Generates unique UUIDs for every user session to maintain distinct conversation threads.

# Prerequisites
* Python 3.10 or higher

* Ollama Desktop (Download from ollama.com)

* Windows PowerShell or Terminal

# Installation
 Activate the Virtual Environment:

PowerShell
    .\venv\Scripts\activate 
Install Required Packages:

Bash

    pip install langchain-ollama langchain-community langchain-core chromadb fastapi uvicorn streamlit python-dotenv requests


# Local Model Setup
This project requires specific models to be available locally via Ollama. Run the following commands:

PowerShell

    <!-- Pull the Llama3 model for text generation -->
    ollama pull llama3
    <!-- Pull the mxbai embedding model for vector search -->
    ollama pull mxbai-embed-large

# Running the Application
You must keep two separate terminals running at the same time.

1. Start the Backend (API)
The backend manages the AI logic, vector search, and database.

PowerShell

    uvicorn app.main:app --reload

Once started, view the API documentation at: http://127.0.0.1:8000/docs
2. Start the Frontend (UI)
The frontend provides the interactive chat bubble interface.

PowerShell

In a new terminal tab
    streamlit run frontend.py
Access the chat interface at: http://localhost:8501

# Prompt Engineering & Logic
The bot follows a strict hierarchical reasoning process:

FAQ Search: It first searches the faqs.json vector index.

Contextual Memory: It retrieves the last few messages from sessions.db to understand the conversation flow.

Reasoning: If a match is found, it provides the answer. If no match is found, it uses general knowledge or triggers the Escalation Protocol.

Next Steps: Every response is programmed to suggest a "Next Action" to guide the customer.

# Maintenance
If you update the faqs.json file:

Stop the Backend (Ctrl+C).

Delete the data/chroma_db/ folder.

Restart the Backend; it will automatically re-index the new FAQs into the vector store.