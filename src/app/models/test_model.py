from sqlalchemy import Column, Integer, String
from src.app.databse.database import Base

class TestModel(Base):
    __tablename__ = "test_table"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
