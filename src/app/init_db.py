from src.app.database import Base, engine
from src.app.models.test_model import TestModel

# Crear las tablas en la base de datos
print("Creando tablas...")
Base.metadata.create_all(bind=engine)
print("Tablas creadas.")
