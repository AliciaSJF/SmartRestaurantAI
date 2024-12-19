from datetime import datetime, time
from typing import Iterable
from sqlalchemy.orm import Session
from src.app.models.restaurant import MenuItem, Reservation
from src.app.databse.database import get_db
from langchain_core.tools import tool
from src.app.utils.state import State
import logging


logger = logging.getLogger(__name__)

@tool
def get_menu() -> str:
    """Devuelve el menú actual del restaurante."""
    logger.info("Entrando a get_menu")
    try:
        with next(get_db()) as db:
            items = db.query(MenuItem).all()
            if not items:
                return "El menú está vacío en este momento."
            logger.info("Saliendo de get_menu")
            return "\n".join([f"{item.name} - {item.price}€ - {item.category}" for item in items])
    except Exception as e:
        logger.error(f"Error en get_menu: {e}")
        return "Ocurrió un error al obtener el menú. Por favor, inténtalo de nuevo más tarde."

    
@tool 
def get_menu_with_ingredients() ->str:
    """Devuelve el menú con los ingredientes de cada plato."""
    logger.info("Entrando a get_menu_with_ingredients")
    try:
        with next(get_db()) as db:
            items = db.query(MenuItem).all()
            if not items:
                return "El menú está vacío en este momento."
            menu = "\n".join([f"{item.name} - {item.price}€ - {item.category}, Ingredients: {item.ingredients} ,Allergens: {item.allergens}" for item in items])
        return f"Este es el menú actual con los ingredientes:\n{menu}"
    except Exception as e:
        logger.error(f"Error en get_menu_with_ingredients: {e}")
        return "Ocurrió un error al obtener el menú con ingredientes. Por favor, inténtalo de nuevo más tarde."
    
@tool
def get_menu_item(dish: str) -> str:
    """Devuelve un plato específico del menú."""
    logger.info("Entrando a get_menu_item")
    with next(get_db()) as db:
        item = db.query(MenuItem).filter(MenuItem.name == dish).first()
        if not item:
            return "No se encontró el plato especificado."
        print(item)
        return f"{item.name} - {item.price}€ - {item.category}, Ingredients: {item.ingredients}, Allergens: {item.allergens}"

@tool
def create_reservation(name: str, guests: int) -> str:
    """Crea una reserva en la base de datos."""
  
    default_date = datetime.today().date() 
    default_time = time(hour=19, minute=0)  
    default_table_capacity = guests  

    with next(get_db()) as db: 
        new_reservation = Reservation(
            restaurant_id=1,  
            name=name,
            date=default_date,
            time=default_time,
            guests=guests,
            table_capacity=default_table_capacity
        )
        db.add(new_reservation)
        db.commit()
    return f"Reserva creada con éxito para {name}, {guests} personas, el {default_date} a las {default_time}."



@tool
def add_to_order(dish: str, quantity: int) -> str:
    """Añade un plato al pedido actual.
    return f"Se añadió {quantity} x {dish} al pedido.
    """
    logger.info("Entrando a add_to_order")

@tool
def confirm_order() -> str:
    """Confirma el pedido actual con el cliente
    return "¿Es correcto el pedido? Por favor, confírmalo.
    """
    logger.info("Entrando a confirm_order")
   
@tool
def get_order() -> str:
    """Devuelve el pedido del cliente ."""
    logger.info("Entrando a get_order")

@tool
def clear_order():
    """Elimina el pedido actual."""
    logger.info("Entrando a clear_order")

@tool
def place_order() -> str:
    """Envía el pedido y devuelve el tiempo estimado.
        return "Pedido enviado a la cocina. Estará listo en 15 minutos.
    """
    logger.info("Entrando a place_order")
