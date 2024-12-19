
# src/app/routers/chat_router.py
import os
import uuid
from fastapi import APIRouter, Cookie, HTTPException, FastAPI, Response
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
async def chat_with_bot(
    query: UserQuery, 
    response: Response, 
    thread_id: str = Cookie(None) 
):
    try:
        if not thread_id:
            thread_id = str(uuid.uuid4())
            response.set_cookie(key="thread_id", value=thread_id)  
        answer = ask_langgraph_agent(query.question, thread_id)
        return {"response": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
                                                                                                                                                                                                                                                                                                                          
# @router.get("/")
# async def get_home(
#     response: Response, 
#     thread_id: str = Cookie(None) 
# ):
#     try:
#         if not thread_id:
#             thread_id = str(uuid.uuid4())
#             response.set_cookie(key="thread_id", value=thread_id)
#         # Obtén la respuesta del chatbot
#         answer = first_message(thread_id)
        
#         # Carga la vista HTML
#         html_path = os.path.join(os.path.dirname(__file__), "../static/index.html")
#         with open(html_path, "r") as file:
#             html_content = file.read()
        
#         # Incluye la respuesta del chatbot en la vista HTML
#         html_content = html_content.replace("{{ chatbot_response }}", answer)
        
#         return HTMLResponse(content=html_content)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
                                                                