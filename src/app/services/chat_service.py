# src/app/services/chat_service.py
from openai import OpenAI
from src.app.core.config import load_config
import openai

# Inicializa el cliente OpenAI
openai.api_key = load_config()["api_key"]

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
