from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from openai import OpenAI
import json
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Inicializar FastAPI
app = FastAPI()

# Cargar información del restaurante desde un archivo JSON
with open(os.path.join(os.path.dirname(__file__), "restaurant_info.json"), "r") as file:
    restaurant_data = json.load(file)

# Inicializar cliente de OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Modelo Pydantic para la entrada del usuario
class UserQuery(BaseModel):
    question: str

# Endpoint para manejar el chat
@app.post("/chat")
async def chat_with_bot(query: UserQuery):
    prompt = f"""
    Eres un asistente virtual para el restaurante {restaurant_data['name']}.
    Responde solo con la información proporcionada. 
    Si no tienes la respuesta, indica que no sabes la respuesta.

    Información del restaurante:
    - Menú: {restaurant_data['menu']}
    - Horarios: {restaurant_data['horarios']}
    - Ubicación: {restaurant_data['ubicacion']}

    Pregunta: {query.question}
    """
    try:
        # Llamar a la API de OpenAI con el cliente
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un asistente especializado en restaurantes."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=100,
            temperature=0.7
        )
        # Extraer la respuesta generada por el modelo
        return {"response": completion.choices[0].message.content.strip()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para servir el archivo index.html
@app.get("/")
async def get_home():
    return FileResponse(os.path.join(os.path.dirname(__file__), "static/index.html"))

# Montar la carpeta estática
static_path = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_path), name="static")
