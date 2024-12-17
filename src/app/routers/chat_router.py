
# src/app/routers/chat_router.py
import os
from fastapi import APIRouter, HTTPException, FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from src.app.services.chat_service import ask_chatbot
from src.app.services.chat_service import ask_langgraph_agent

router = APIRouter()

class UserQuery(BaseModel):
    question: str


    
@router.get("/")
async def get_home():
    return FileResponse(os.path.join(os.path.dirname(__file__), "../static/index.html"))


@router.post("/chat")
async def chat_with_bot(query: UserQuery):
    try:
        response = ask_langgraph_agent(query.question)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
                                                                                                                                                                                                                                                                                                                                  