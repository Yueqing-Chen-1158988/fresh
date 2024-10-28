from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash
from models.base import Base

class Customer(Base):
    __tablename__ = 'customers'
    
    customer_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(25), nullable=False)
    username = Column(String(25), unique=True, nullable=False)
    password_hash = Column(String(256), nullable=False) 
    email = Column(String(50), unique=True, nullable=False)
    balance = Column(Float, default=0.0)
    
    orders = relationship('Order', back_populates='customer')

    def __init__(self, name, username, email, password, balance=0.0):
        self.name = name
        self.username = username
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.balance = balance
    
    def __str__(self):
        return f"Customer({self.name}, {self.email}, Balance: {self.balance})"


class CorporateCustomer(Customer):
    __tablename__ = 'corporate_customers'
    
    customer_id = Column(Integer, ForeignKey('customers.customer_id'), primary_key=True)
    credit_limit = Column(Float, nullable=False)
    discount_rate = Column(Float, nullable=False)
    
    def __init__(self, name, username, email, password, balance, credit_limit, discount_rate):
        super().__init__(name, username, email, password, balance)
        self.credit_limit = credit_limit
        self.discount_rate = discount_rate
    
    def __str__(self):
        return f"CorporateCustomer({self.name}, {self.email}, Balance: {self.balance}, Credit Limit: {self.credit_limit}, Discount: {self.discount_rate})"