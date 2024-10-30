import pytest
from datetime import datetime, timedelta
from sqlalchemy import func
from models.customer import Customer, CorporateCustomer
from models.order import Order
from models.order_line import OrderLine
from models.vegetable_premadeBox import Vegetable, PremadeBox
from controllers.staff_controller import StaffController

@pytest.fixture
def staff_controller(session):
    return StaffController(session)

def test_get_all_vegetables(staff_controller, session):
    # Seed data
    veg1 = Vegetable(name="Carrot", price_per_unit=2.5, unit="kg")
    veg2 = Vegetable(name="Tomato", price_per_unit=3.0, unit="kg")
    session.add_all([veg1, veg2])
    session.commit()

    # Test
    vegetables = staff_controller.get_all_vegetables()
    assert len(vegetables) == 2
    assert vegetables[0].name == "Carrot"

def test_get_all_premade_boxes(staff_controller, session):
    # Seed data
    box1 = PremadeBox(size="Small Box", price=10.0)
    box2 = PremadeBox(size="Large Box", price=20.0)
    session.add_all([box1, box2])
    session.commit()

    # Test
    premade_boxes = staff_controller.get_all_premade_boxes()
    assert len(premade_boxes) == 2
    assert premade_boxes[0].size == "Small Box"

def test_get_orders_by_type(staff_controller, session, seed_data):
    # Use the customer_id from the created customer
    customer_id = seed_data.customer_id

    # Seed orders
    order1 = Order(customer_id=customer_id, status="Processing")
    order2 = Order(customer_id=customer_id, status="Completed")
    session.add_all([order1, order2])
    session.commit()

    # Test for current orders
    current_orders = staff_controller.get_orders_by_type("Current Orders")
    assert len(current_orders) == 1
    assert current_orders[0].status == "Processing"

    # Test for previous orders
    previous_orders = staff_controller.get_orders_by_type("Previous Orders")
    assert len(previous_orders) == 1
    assert previous_orders[0].status == "Completed"

def test_get_order_total(staff_controller, session, seed_data):
    # Use the customer_id from the seeded customer
    customer_id = seed_data.customer_id

    # Seed order data
    order = Order(customer_id=customer_id, delivery_fee=5.0)
    line1 = OrderLine(order_id=order.order_id, item_type="Vegetable", item_name="Carrot", quantity=2, price=2.5)
    line2 = OrderLine(order_id=order.order_id, item_type="Premade Box", item_name="Small Box", quantity=1, price=10.0)
    order.order_lines.extend([line1, line2])
    session.add(order)
    session.commit()

    # Test
    total = staff_controller.get_order_total(order)
    assert total == 20.0  # 2 * 2.5 + 1 * 10.0 + 5.0

def test_get_order_detail(staff_controller, session, seed_data):
    # Use the customer_id from the seeded customer
    customer_id = seed_data.customer_id

    # Seed order data
    order = Order(customer_id=customer_id, delivery_option="Delivery", delivery_fee=5.0)
    
    # Add the order to the session first to get its order_id
    session.add(order)
    session.commit()  # Commit to get the order_id assigned

    # Now create the OrderLine with the order_id
    line1 = OrderLine(order_id=order.order_id, item_type="Vegetable", item_name="Carrot", quantity=2, price=2.5)
    
    # Add the order line to the session
    session.add(line1)
    session.commit()

    # Test
    details = staff_controller.get_order_detail(order.order_id)
    assert details["delivery_fee"] == 5.0
    assert len(details["order_lines"]) == 1
    assert details["order_lines"][0]["item_name"] == "Carrot"


def test_update_order_status(staff_controller, session, seed_data):
    # Use the customer_id from the seeded customer
    customer_id = seed_data.customer_id
    
    # Seed order with the customer_id
    order = Order(customer_id=customer_id, status="Processing")
    session.add(order)
    session.commit()

    # Test status update
    result = staff_controller.update_order_status(order.order_id, "Completed")
    
    # Refresh the order to get the latest status from the database
    session.refresh(order)
    
    assert result is True
    assert order.status == "Completed"

def test_get_all_customers(staff_controller, session):
    # Seed customers
    customer = Customer(name="Emily", username="emily123", email="emily@123.com", password="password")
    session.add(customer)

    corporate_customer = CorporateCustomer(
        name="BobCorp",
        username="bob123",
        email="bob@123.com",
        password="password",
        balance=500.0,
        credit_limit=1000.0,
        discount_rate=0.1
    )
    session.add(corporate_customer)
    session.commit()

    # Test getting all customers
    customers = staff_controller.get_all_customers()

    expected_customers = [
        {"name": "Emily", "username": "emily123", "email": "emily@123.com"},
        {"name": "BobCorp", "username": "bob123", "email": "bob@123.com", "credit_limit": 1000.0, "discount_rate": 0.1},
    ]

    # Check if the returned customers match the expected data
    for expected in expected_customers:
        assert any(
            c.name == expected["name"] and c.username == expected["username"] and 
            (not expected.get("credit_limit") or c.credit_limit == expected["credit_limit"]) and 
            (not expected.get("discount_rate") or c.discount_rate == expected["discount_rate"]) 
            for c in customers
        )


def test_get_customers_by_name(staff_controller, session):
    # Seed data
    customer1 = Customer(name="Alice")
    customer2 = Customer(name="Bob")
    session.add_all([customer1, customer2])
    session.commit()

    # Test
    results = staff_controller.get_customers_by_name("Alice")
    assert len(results) == 1
    assert results[0].name == "Alice"

def test_generate_sales_report(staff_controller, session):
    # Seed data
    now = datetime.now()
    order = Order(order_date=now)
    line = OrderLine(order_id=1, item_type="Vegetable", item_name="Carrot", quantity=3, price=2.0)
    order.order_lines.append(line)
    session.add(order)
    session.commit()

    # Test for weekly sales report
    sales_report = staff_controller.generate_sales_report("Week")
    assert len(sales_report) > 0
    assert sales_report[-1][0] == "Total Sales"

def test_get_popular_items(staff_controller, session):
    # Seed data
    line1 = OrderLine(item_name="Carrot", quantity=3)
    line2 = OrderLine(item_name="Carrot", quantity=2)
    line3 = OrderLine(item_name="Tomato", quantity=5)
    session.add_all([line1, line2, line3])
    session.commit()

    # Test
    popular_items = staff_controller.get_popular_items()
    assert popular_items[0][0] == "Carrot"
    assert popular_items[0][1] == 2  # Carrot appears in two orders
