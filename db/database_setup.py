from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base import Base
from models.customer import Customer, CorporateCustomer
from models.staff import Staff
from models.vegetable_premadeBox import Vegetable, PremadeBox 
from models.order import Order
from models.order_line import OrderLine
from models.payment import Payment

# Database URL
DATABASE_URL = 'mysql+pymysql://root:cyq123..@localhost/fresh'

# Create the engine
engine = create_engine(DATABASE_URL, echo=True)

# Create a configured session class
SessionLocal = sessionmaker(bind=engine)

# Function to drop all tables
def drop_tables():
    Base.metadata.drop_all(bind=engine)
    print("All tables dropped successfully.")

# Create all tables (will create them in the connected database)
def create_tables():
    Base.metadata.create_all(bind=engine)

# Create session function
def get_session():
    return SessionLocal()
