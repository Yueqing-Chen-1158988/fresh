from sqlalchemy import Column, Integer, Float, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from models.base import Base

class Order(Base):
    __tablename__ = 'orders'
    
    order_id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customers.customer_id'), nullable=False)
    order_type = Column(Enum('vegetable', 'premade_box', name='order_type_enum'), nullable=False)
    order_date = Column(DateTime, default=datetime.now)
    status = Column(Enum('processing', 'completed', 'delivered', name='order_status_enum'), default='processing')
    delivery_option = Column(Enum('collect', 'delivery', name='delivery_option_enum'), default='collect')
    delivery_fee = Column(Float, default=0.0)
    
    customer = relationship('Customer', back_populates='orders')
    order_lines = relationship('OrderLine', back_populates='order')
    payments = relationship('Payment', back_populates='order')

    def __init__(self, customer_id, order_type, delivery_option='collect', delivery_fee=0.0, status='processing'):
        self.customer_id = customer_id
        self.order_type = order_type
        self.delivery_option = delivery_option
        self.delivery_fee = delivery_fee
        self.status = status
    
    def __str__(self):
        return f"Order({self.order_id}, Customer: {self.customer_id}, Type: {self.order_type}, Status: {self.status})"
