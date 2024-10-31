from sqlalchemy import Column, Integer, String, Float, Enum, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base

class Vegetable(Base):
    __tablename__ = 'vegetables'
    
    vegetable_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    price_per_unit = Column(Float, nullable=False)
    unit = Column(String(25), nullable=False)  # e.g., 'kg', 'pack', 'unit'

    # Relationship to contents, linking with premade boxes
    boxes = relationship("Contents", back_populates="vegetable")

    def __init__(self, name, price_per_unit, unit):
        self.name = name
        self.price_per_unit = price_per_unit
        self.unit = unit
    
    def __str__(self):
        return f"Vegetable({self.name}, Price per {self.unit}: {self.price_per_unit})"


class PremadeBox(Base):
    __tablename__ = 'premade_boxes'
    
    box_id = Column(Integer, primary_key=True, autoincrement=True)
    size = Column(Enum('Small Box', 'Medium Box', 'Large Box', name='box_size_enum'), nullable=False)
    price = Column(Float, nullable=False)

    # Relationship to contents, establishing a link with vegetables
    contents = relationship("Contents", back_populates="box")
    
    def __init__(self, size, price):
        self.size = size
        self.price = price
    
    def __str__(self):
        return f"PremadeBox(Size: {self.size}, Price: {self.price})"

class Contents(Base):
    __tablename__ = 'contents'
    
    content_id = Column(Integer, primary_key=True, autoincrement=True)
    box_id = Column(Integer, ForeignKey('premade_boxes.box_id'), nullable=False)
    vegetable_id = Column(Integer, ForeignKey('vegetables.vegetable_id'), nullable=False)
    quantity = Column(Float, nullable=False) 
    
    # Relationships to link contents back to box and vegetable
    box = relationship("PremadeBox", back_populates="contents")
    vegetable = relationship("Vegetable", back_populates="boxes")
    
    def __init__(self, box_id, vegetable_id, quantity):
        self.box_id = box_id
        self.vegetable_id = vegetable_id
        self.quantity = quantity

    def __str__(self):
        return f"Contents(Box ID: {self.box_id}, Vegetable ID: {self.vegetable_id}, Quantity: {self.quantity})"