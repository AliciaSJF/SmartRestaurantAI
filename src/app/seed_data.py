from src.app.databse.database import SessionLocal
from models.restaurant import Restaurant, Menu, Reservation, MenuItem
#TODO: python -m src.app.seed_data

db = SessionLocal()


db = SessionLocal()

# Insertar restaurante
restaurant = Restaurant(
    name="Monitolandia",
    address="Calle del monito 123",
    phone="+123456789",
    email="restaurante@monitos.com",
    capacity_total=100,
    capacity_reservable=50
)
db.add(restaurant)
db.commit()

# Insertar menú
menu = Menu(restaurant_id=restaurant.id)
db.add(menu)
db.commit()

# Insertar platos

# Insertar platos italianos con categorías
items = [
    # Antipasti
    MenuItem(
        menu_id=menu.id,
        name="Bruschetta",
        price=5.5,
        ingredients="pan, tomate, ajo, albahaca, aceite de oliva",
        allergens="gluten",
        category="antipasti"
    ),
    MenuItem(
        menu_id=menu.id,
        name="Caprese",
        price=8.0,
        ingredients="mozzarella, tomate, albahaca, aceite de oliva",
        allergens="lácteos",
        category="antipasti"
    ),
    # Primi Piatti
    MenuItem(
        menu_id=menu.id,
        name="Spaghetti Carbonara",
        price=12.0,
        ingredients="spaghetti, huevo, queso pecorino, panceta, pimienta",
        allergens="gluten, huevo, lácteos",
        category="primi piatti"
    ),
    MenuItem(
        menu_id=menu.id,
        name="Risotto ai Funghi",
        price=14.0,
        ingredients="arroz, setas porcini, cebolla, vino blanco, parmesano",
        allergens="lácteos",
        category="primi piatti"
    ),
    # Dolci
    MenuItem(
        menu_id=menu.id,
        name="Tiramisù",
        price=6.5,
        ingredients="mascarpone, huevo, café, cacao, bizcocho",
        allergens="gluten, huevo, lácteos",
        category="dolci"
    ),
    MenuItem(
        menu_id=menu.id,
        name="Panna Cotta",
        price=5.5,
        ingredients="nata, azúcar, gelatina, frutos rojos",
        allergens="lácteos",
        category="dolci"
    )
]
db.add_all(items)
db.commit()

# Insertar reserva
reservation = Reservation(
    restaurant_id=restaurant.id,
    name="Juan Pérez",
    date="2024-11-30",
    time="20:00",
    guests=4,
    table_capacity=4
)
db.add(reservation)
db.commit()

print("Datos iniciales insertados.")