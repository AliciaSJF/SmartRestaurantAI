from sqlalchemy import Column, Integer, String, ForeignKey, Float, Table, Date, Time, JSON, Enum
from sqlalchemy.orm import relationship
from database import Base
#from src.app.database import Base #para alembic
#from src.app.enums import MenuCategory  # Importar el Enum #para alembic
from enums import MenuCategory


class Restaurant(Base):
    __tablename__ = "restaurant"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    capacity_total = Column(Integer, nullable=False)  # Aforo máximo
    capacity_reservable = Column(Integer, nullable=False)  # Aforo reservable

    # Relación con el menú
    menu = relationship("Menu", back_populates="restaurant", uselist=False)

    # Relación con las reservas
    reservations = relationship("Reservation", back_populates="restaurant")

class Menu(Base):
    __tablename__ = "menu"

    id = Column(Integer, primary_key=True, autoincrement=True)
    restaurant_id = Column(Integer, ForeignKey("restaurant.id"), nullable=False)
    # Relación con el restaurante
    restaurant = relationship("Restaurant", back_populates="menu")

    # Relación con los platos del menú
    items = relationship("MenuItem", back_populates="menu")


class MenuItem(Base):
    __tablename__ = "menu_item"

    id = Column(Integer, primary_key=True, autoincrement=True)
    menu_id = Column(Integer, ForeignKey("menu.id"), nullable=False)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    ingredients = Column(String, nullable=False)  # Separados por comas
    allergens = Column(String, nullable=True)  # Separados por comas
    category = Column(Enum(MenuCategory), nullable=False)  # Campo Enum para las categorías


    # Relación con el menú
    menu = relationship("Menu", back_populates="items")

class Reservation(Base):
    __tablename__ = "reservation"

    id = Column(Integer, primary_key=True, autoincrement=True)
    restaurant_id = Column(Integer, ForeignKey("restaurant.id"), nullable=False)
    name = Column(String, nullable=False)  # Nombre del cliente
    date = Column(Date, nullable=False)  # Fecha de la reserva
    time = Column(Time, nullable=False)  # Hora de la reserva
    guests = Column(Integer, nullable=False)  # Número de comensales
    table_capacity = Column(Integer, nullable=False)  # Espacio reservado

    # Relación con el restaurante
    restaurant = relationship("Restaurant", back_populates="reservations")
