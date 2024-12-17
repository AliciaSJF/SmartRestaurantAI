from unittest.mock import Base
from enum import Enum  # Enum de Python
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
from datetime import datetime
from src.app.databse.database import Base  # Asegúrate de que Base esté correctamente definido

# Enum de Python
class OrderStatus(Enum):
    PENDING = "pending"
    PREPARING = "preparing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

# Modelo de SQLAlchemy para las órdenes
class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_name = Column(String, nullable=False)
    customer_phone = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    # Usa SQLAlchemyEnum para la columna de estado
    status = Column(SQLAlchemyEnum(OrderStatus), default=OrderStatus.PENDING, nullable=False)

    # Relación con los platos
    items = relationship("OrderItem", back_populates="order")

# Modelo de SQLAlchemy para los ítems del pedido
class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    menu_item_id = Column(Integer, ForeignKey("menu_item.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)  # Precio unitario al momento del pedido

    # Relación con el pedido
    order = relationship("Order", back_populates="items")

    # Relación con el menú
    menu_item = relationship("MenuItem")
