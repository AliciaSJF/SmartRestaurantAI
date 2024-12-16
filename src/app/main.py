import os
import sys
import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from src.app.core.config import load_config
from src.app.routers import chat_router
from src.app.databse.database import engine, Base, get_db
from src.app.services.chat_service import ask_chatbot
from src.app.core.logger import logger
import uvicorn


# Cargar variables de entorno desde el archivo .env
load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Eventos de inicio y apagado."""
    logger.info("Inicializando la aplicación.")
    logger.info("Conectando a la base de datos: %s", os.getenv("DATABASE_URL"))
    try:
        # Configuración inicial, como modelos o datos pre-cargados
        app.state.db_session = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=engine,
            class_=AsyncSession,
        )
        logger.info("Base de datos inicializada.")
        yield
    finally:
        logger.info("Cerrando la aplicación.")
        await engine.dispose()


# Inicializar FastAPI con lifespan
app = FastAPI(lifespan=lifespan)
# Configurar middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
# app.include_router(restaurant_router.router, prefix="/restaurants", tags=["Restaurants"])
# app.include_router(menu_router.router, prefix="/menus", tags=["Menus"])
# app.include_router(reservation_router.router, prefix="/reservations", tags=["Reservations"])
# app.include_router(order_router.router, prefix="/orders", tags=["Orders"])
app.include_router(chat_router.router, prefix="/api", tags=["Chat"])

# Servir archivos estáticos
app.mount("/static", StaticFiles(directory="src/app/static"), name="static")

if __name__ == "__main__":
    uvicorn.run(app, host=os.getenv("HOST", "127.0.0.1"), port=os.getenv("PORT", 8000))



