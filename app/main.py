from fastapi import FastAPI
from pydantic import BaseModel
from .agent import SupportAgent
from .database import init_db

app = FastAPI(title="AI Support Bot API")
agent = SupportAgent()

@app.on_event("startup")
async def startup():
    init_db()

class ChatRequest(BaseModel):
    message: str
    session_id: str

@app.post("/chat")
async def chat(request: ChatRequest):
    bot_response = agent.run(request.message, request.session_id)
    return {"bot_response": bot_response}