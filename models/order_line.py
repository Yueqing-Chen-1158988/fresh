from sqlalchemy import Column, Integer, String, Float, Enum, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base

class OrderLine(Base):
    __tablename__ = 'order_lines'
    
    line_id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('orders.order_id'), nullable=False)
    item_type = Column(Enum('Vegetable', 'Premade Box', name='item_type_enum'), nullable=False)
    item_name = Column(String(100), nullable=False)  # This can represent either a vegetable or a premade box
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    
    order = relationship('Order', back_populates='order_lines')

    def __init__(self, order_id, item_type, item_name, quantity, price):
        self.order_id = order_id
        self.item_type = item_type
        self.item_name = item_name
        self.quantity = quantity
        self.price = price
    
    def __str__(self):
        return f"OrderLine(Item: {self.item_name}, Quantity: {self.quantity}, Price: {self.price})"
