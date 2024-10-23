from sqlalchemy import Column, Integer, String, Float, Enum, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base

class Vegetable(Base):
    __tablename__ = 'vegetables'
    
    vegetable_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    price_per_unit = Column(Float, nullable=False)
    unit = Column(String(25), nullable=False)  # e.g., 'kg', 'pack', 'unit'

    def __init__(self, name, price_per_unit, unit):
        self.name = name
        self.price_per_unit = price_per_unit
        self.unit = unit
    
    def __str__(self):
        return f"Vegetable({self.name}, Price per {self.unit}: {self.price_per_unit})"


class PremadeBox(Base):
    __tablename__ = 'premade_boxes'
    
    box_id = Column(Integer, primary_key=True, autoincrement=True)
    size = Column(Enum('small', 'medium', 'large', name='box_size_enum'), nullable=False)
    price = Column(Float, nullable=False)

    def __init__(self, size, price):
        self.size = size
        self.price = price
    
    def __str__(self):
        return f"PremadeBox(Size: {self.size}, Price: {self.price})"
