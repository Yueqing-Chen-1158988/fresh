import pytest
from models.staff import Staff

@pytest.fixture
def test_staff_init():
    staff = Staff("Emma Blank", "emma@123.com", "emma", "password")
    assert staff.name == "Emma Blank"
    assert staff.email == "emma@123.com"
    assert staff.username == "emma"
    assert staff.password_hash != "password"

def test_staff_check_password():
    staff = Staff("Emma Blank", "emma@123.com", "emma", "password")
    assert staff.check_password("password") == True
    assert staff.check_password("wrongpassword") == False

def test_staff_str():
    staff = Staff("Emma Blank", "emma@123.com", "emma", "password")
    assert str(staff) == "Staff(Emma Blank, emma@123.com)"
