from sqlalchemy import Column, Integer, Float, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from models.base import Base

class Order(Base):
    __tablename__ = 'orders'
    
    order_id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customers.customer_id'), nullable=False)
    staff_id = Column(Integer, ForeignKey('staff.staff_id'))
    # order_type = Column(Enum('vegetable', 'premade_box', name='order_type_enum'), nullable=False)
    order_date = Column(DateTime, default=datetime.now)
    status = Column(Enum('Processing', 'Completed', 'Cancelled', name='order_status_enum'), default='Processing')
    delivery_option = Column(Enum('Collect', 'Delivery', name='delivery_option_enum'), default='Collect')
    delivery_fee = Column(Float, default=0.0)
    
    customer = relationship('Customer', back_populates='orders')
    staff = relationship('Staff', back_populates='orders')
    order_lines = relationship('OrderLine', back_populates='order')
    payments = relationship('Payment', back_populates='order')

    def __init__(self, customer_id, delivery_option='Collect', delivery_fee=0.0, staff_id=None, status='Processing'):
        self.customer_id = customer_id
        self.staff_id = staff_id
        self.delivery_option = delivery_option
        self.delivery_fee = delivery_fee
        self.status = status
    
    def __str__(self):
        return f"Order({self.order_id}, Customer: {self.customer_id}, Status: {self.status})"

    # Add a method to cancel orders
    def cancel_order(self):
        if self.status in ["Processing"]:
            self.status = "Cancelled"
            