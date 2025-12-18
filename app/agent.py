import json
from langchain_ollama import OllamaLLM, OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.messages import HumanMessage, AIMessage
from .prompts import SUPPORT_PROMPT
from .database import save_message, get_history

class SupportAgent:
    def __init__(self):
        # Modern imports to fix DeprecationWarnings
        self.llm = OllamaLLM(model="llama3")
        self.embeddings = OllamaEmbeddings(model="mxbai-embed-large")
        
        # Load FAQ dataset (Requirement 5)
        with open("data/faqs.json", "r") as f:
            faq_data = json.load(f)
        
        texts = [f"Q: {item['question']} A: {item['answer']}" for item in faq_data]
        
        # Initialize Vector DB (Requirement 5, 20)
        self.vector_db = Chroma.from_texts(
            texts, 
            self.embeddings, 
            persist_directory="./data/chroma_db"
        )
        self.retriever = self.vector_db.as_retriever(search_kwargs={"k": 1})

    def run(self, user_input, session_id):
        # Search FAQ context (Requirement 5)
        docs = self.retriever.invoke(user_input)
        context = docs[0].page_content if docs else "No specific FAQ match found."
        
        # Retrieve persistent history (Requirement 6, 12)
        db_history = get_history(session_id)
        chat_history = []
        for msg in db_history:
            if msg['role'] == 'user': 
                chat_history.append(HumanMessage(content=msg['content']))
            else: 
                chat_history.append(AIMessage(content=msg['content']))

        # Combine logic into the final chain (Requirement 14)
        chain = SUPPORT_PROMPT | self.llm
        response = chain.invoke({
            "input": f"Context from FAQ: {context}\n\nUser Question: {user_input}",
            "chat_history": chat_history
        })

        # Persist session data (Requirement 12, 20)
        save_message(session_id, "user", user_input)
        save_message(session_id, "assistant", response) 

        return response