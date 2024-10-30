from sqlalchemy import Column, Integer, Float, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from models.base import Base

class Payment(Base):
    __tablename__ = 'payments'
    
    payment_id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('orders.order_id'), nullable=False)
    payment_type = Column(Enum('credit_card', 'debit_card', 'account', name='payment_type_enum'), nullable=False)
    amount = Column(Float, nullable=False)
    payment_date = Column(DateTime, default=datetime.now)
    payment_status = Column(Enum('pending', 'completed', 'failed', name='payment_status_enum'), default='pending')

    order = relationship('Order', back_populates='payments')

    def __init__(self, order_id, payment_type, payment_status, amount):
        self.order_id = order_id
        self.payment_type = payment_type
        self.payment_status = payment_status
        self.amount = amount
    
    def __str__(self):
        return f"Payment(Order: {self.order_id}, Type: {self.payment_type}, Status: {self.payment_status}, Amount: {self.amount})"
