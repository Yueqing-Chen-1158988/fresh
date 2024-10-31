import uuid
import pytest
import sys
import os

# Add the project root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database_setup import get_session, create_tables, drop_tables
from models.customer import Customer

# Fixture for setting up the database
@pytest.fixture(scope="session", autouse=True)
def setup_database():
    drop_tables()
    create_tables()
    yield
    drop_tables()

@pytest.fixture
def session():
    db = get_session()
    try:
        yield db
    finally:
        db.rollback()
        db.close()

@pytest.fixture
def seed_data(session):
    unique_username = f"testuser_{uuid.uuid4()}"[:25]
    unique_email = f"test_{uuid.uuid4()}@example.com"[:50]
    customer = Customer(
        name="Test Customer",
        username=unique_username,
        email=unique_email,
        password="password"
    )
    session.add(customer)
    session.commit()
    return customer
