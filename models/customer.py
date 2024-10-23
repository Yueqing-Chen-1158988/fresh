from sqlalchemy import Column, Integer, String, Float, Enum, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base

class Customer(Base):
    __tablename__ = 'customers'
    
    customer_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(25), nullable=False)
    email = Column(String(25), unique=True, nullable=False)
    balance = Column(Float, default=0.0)
    
    orders = relationship('Order', back_populates='customer')

    def __init__(self, name, email, balance=0.0):
        self.name = name
        self.email = email
        self.balance = balance
    
    def __str__(self):
        return f"Customer({self.name}, {self.email}, Balance: {self.balance})"


class CorporateCustomer(Customer):
    __tablename__ = 'corporate_customers'
    
    customer_id = Column(Integer, ForeignKey('customers.customer_id'), primary_key=True)
    credit_limit = Column(Float, nullable=False)
    discount_rate = Column(Float, nullable=False)
    
    def __init__(self, name, email, balance, credit_limit, discount_rate):
        super().__init__(name, email, balance)
        self.credit_limit = credit_limit
        self.discount_rate = discount_rate
    
    def __str__(self):
        return f"CorporateCustomer({self.name}, {self.email}, Balance: {self.balance}, Credit Limit: {self.credit_limit}, Discount: {self.discount_rate})"
