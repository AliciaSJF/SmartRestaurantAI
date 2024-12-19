# src/app/services/chat_service.py
from openai import OpenAI
from src.app.core.config import load_config
import openai
from src.app.agent import chat_graph
import logging
from langchain.schema import HumanMessage


logger = logging.getLogger(__name__)

openai.api_key = load_config()["api_key"]

def ask_langgraph_agent(question: str, thread_id: str) -> str:
    """Inicia el grafo y devuelve la respuesta final."""
    state = {
        "messages": [HumanMessage(content=question)]  }
    config = {
        "configurable": {"thread_id": thread_id} }
    final_state = chat_graph.invoke(state, config) 
    return final_state["messages"][-1].content 

def first_message(thread_id : str) -> str:
    state = {
        "messages": [] }
    config = {
        "configurable": {"thread_id": thread_id} }
    final_state = chat_graph.invoke(state, config)
    logger.info(f"first_message: {final_state}")
    return final_state["messages"][-1].content




def ask_chatbot(question: str) -> str:
    prompt = f"""
    Eres un asistente virtual para el restaurante Alicia.
    Responde solo con la información proporcionada. 
    Si no tienes la respuesta, indica que no sabes la respuesta.
    Está en vallecas, 
    venden batidos, magdalenas y donuts de chocolate, pistacho y vainilla.

    Pregunta: {question}
    """
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un asistente especializado en restaurantes."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=100,
            temperature=0.5
        )
        return response.choices[0].message.content.strip()
    except openai.AuthenticationError as e:
        raise RuntimeError(f"Error de autenticación en OpenAI: {e}")
    except Exception as e:
        raise RuntimeError(f"Error inesperado: {str(e)}")
