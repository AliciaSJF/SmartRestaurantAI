from datetime import datetime, time
from sqlalchemy.orm import Session
from src.app.models.restaurant import MenuItem, Reservation
from src.app.databse.database import get_db
from langchain_core.tools import tool

@tool
def get_menu_items() -> str:
    """Obtiene los ítems del menú desde la base de datos."""

    with next(get_db()) as db:  
        items = db.query(MenuItem).all()
        if not items:
            return "El menú está vacío."
        menu = "\n".join([f"{item.name} - {item.price}€" for item in items])
    return f"Este es el menú actual:\n{menu}"

@tool
def get_menu() -> str:
    """Devuelve el menú actual del restaurante."""
    with next(get_db()) as db:
        items = db.query(MenuItem).all()
        if not items:
            return "El menú está vacío en este momento."
        return "\n".join([f"{item.name} - {item.price}€" for item in items])









@tool
def create_reservation(name: str, guests: int) -> str:
    """Crea una reserva en la base de datos."""
    # Fecha y hora por defecto
    default_date = datetime.today().date()  # Fecha actual
    default_time = time(hour=19, minute=0)  # Hora predeterminada para reservas
    default_table_capacity = guests  # Supongamos que el tamaño de la mesa coincide con los invitados

    with next(get_db()) as db:  # Usar next() para manejar el generador
        new_reservation = Reservation(
            restaurant_id=1,  # Simulación de un restaurante único
            name=name,
            date=default_date,
            time=default_time,
            guests=guests,
            table_capacity=default_table_capacity
        )
        db.add(new_reservation)
        db.commit()
    return f"Reserva creada con éxito para {name}, {guests} personas, el {default_date} a las {default_time}."
