from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from openai import OpenAI
import json
import os
from dotenv import load_dotenv
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from src.app.database import get_db
from src.app.models.test_model import TestModel
from sqlalchemy import text
from src.app.database import engine
import openai




# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Inicializar FastAPI
app = FastAPI()

# Cargar información del restaurante desde un archivo JSON
with open(os.path.join(os.path.dirname(__file__), "restaurant_info.json"), "r") as file:
    restaurant_data = json.load(file)

# Inicializar cliente de OpenAI
api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = os.getenv("OPENAI_API_KEY")
#client = OpenAI(api_key=api_key)
#client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Modelo Pydantic para la entrada del usuario
class UserQuery(BaseModel):
    question: str

@app.post("/chat")
async def chat_with_bot(query: UserQuery):
    print("Pregunta del usuario:", query.question)
    print(api_key)
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
        # Nueva forma de llamada a la API de OpenAI
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un asistente especializado en restaurantes."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=100,
            temperature=0.5
        )
        # Acceder a la respuesta usando notación de punto
        content = response.choices[0].message.content.strip()
        return {"response": content}
    except openai.AuthenticationError as e:
        raise HTTPException(status_code=500, detail=f"Error en la API de OpenAI: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

# Endpoint para servir el archivo index.html
@app.get("/")
async def get_home():
    return FileResponse(os.path.join(os.path.dirname(__file__), "static/index.html"))

# Montar la carpeta estática
static_path = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_path), name="static")

@app.post("/test")
def create_test_item(name: str, description: str, db: Session = Depends(get_db)):
    item = TestModel(name=name, description=description)
    db.add(item)
    db.commit()
    db.refresh(item)
    return {"id": item.id, "name": item.name, "description": item.description}

print("Probando conexión a la base de datos...")
try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        print("Conexión exitosa:", result.scalar())
except Exception as e:
    print("Error al conectar con la base de datos:", e)