from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from models.base import Base
from werkzeug.security import generate_password_hash, check_password_hash

class Staff(Base):
    __tablename__ = 'staff'
    
    staff_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(25), nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    username = Column(String(25), unique=True, nullable=False)
    password_hash = Column(String(256), nullable=False)
    
    orders = relationship('Order', back_populates='staff')

    def __init__(self, name, email, username, password):
        self.name = name
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __str__(self):
        return f"Staff({self.name}, {self.email})"
