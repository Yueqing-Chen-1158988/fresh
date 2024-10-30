import pytest
from controllers.customer_controller import CustomerController
from models.customer import Customer
from models.order import Order
from models.order_line import OrderLine
from models.payment import Payment
from models.vegetable_premadeBox import Vegetable, PremadeBox
from unittest.mock import MagicMock, patch
from tkinter import Label

@pytest.fixture
def customer_controller(session):
    return CustomerController(session)

def test_get_vegetable_names(customer_controller, session):
    # Seed data
    veg1 = Vegetable(name="Carrot", price_per_unit=2.5, unit="kg")
    veg2 = Vegetable(name="Tomato", price_per_unit=3.0, unit="kg")
    session.add_all([veg1, veg2])
    session.commit()

    # Test
    names = customer_controller.get_vegetable_names(session)
    assert names == ["Carrot", "Tomato"]

def test_get_premade_box_sizes(customer_controller, session):
    # Seed data
    box1 = PremadeBox(size="Small Box", price=10.0)
    box2 = PremadeBox(size="Large Box", price=20.0)
    session.add_all([box1, box2])
    session.commit()

    # Test
    sizes = customer_controller.get_premade_box_sizes(session)
    assert sizes == ["Small Box", "Large Box"]

def test_update_vegetable_info(customer_controller, session):
    # Seed data
    vegetable = Vegetable(name="Lettuce", price_per_unit=1.5, unit="bunch")
    session.add(vegetable)
    session.commit()

    # Mock UI components
    vegetable_combobox = MagicMock()
    vegetable_combobox.get.return_value = "Lettuce"
    price_label = Label(text="")
    unit_label = Label(text="")

    # Test
    customer_controller.update_vegetable_info(None, session, vegetable_combobox, price_label, unit_label)
    assert price_label["text"] == "$1.50"
    assert unit_label["text"] == "bunch"

def test_add_item_to_cart(customer_controller):
    # Test valid item addition
    cart = []
    item = customer_controller.add_item_to_cart(cart, "Vegetable", "Carrot", "3", "2.5")
    assert item is not None
    assert len(cart) == 1
    assert cart[0]["subtotal"] == 7.5

    # Test invalid quantity
    item = customer_controller.add_item_to_cart(cart, "Vegetable", "Carrot", "-1", "2.5")
    assert item is None
    assert len(cart) == 1

def test_calculate_cart_totals(customer_controller):
    cart = [
        {"type": "Vegetable", "name": "Carrot", "quantity": 2, "price": 2.5, "subtotal": 5.0},
        {"type": "Box", "name": "Small Box", "quantity": 1, "price": 10.0, "subtotal": 10.0}
    ]
    total = customer_controller.calculate_cart_totals(cart)
    assert total == 15.0

def test_submit_order(customer_controller, session, seed_data):
    # Seed customer
    customer_id = seed_data.customer_id

    # Cart data
    cart = [
        {"type": "Vegetable", "name": "Carrot", "quantity": 3, "price": 2.5, "subtotal": 7.5}
    ]
    order_id = customer_controller.submit_order(session, customer_id, cart, "Delivery", 5.0)
    order = session.query(Order).filter_by(order_id=order_id).first()

    # Test order creation
    assert order is not None
    assert order.delivery_option == "Delivery"
    assert order.delivery_fee == 5.0
    assert len(order.order_lines) == 1

def test_load_order_history(customer_controller, session, seed_data):
    # Seed customer
    customer_id = seed_data.customer_id

    # Seed order
    order = Order(customer_id=customer_id, delivery_option="Delivery", delivery_fee=5.0, status="Completed")
    session.add(order)
    session.commit()

    # Test loading order history
    history = customer_controller.load_order_history(session, customer_id)
    assert len(history) == 1
    assert history[0][3] == "Completed"

def test_cancel_order(customer_controller, session):
    # Seed order in "Processing" status
    order = Order(customer_id=1, status="Processing")
    session.add(order)
    session.commit()

    # Test canceling order
    result = customer_controller.cancel_order(session, order.order_id)
    session.refresh(order)
    assert result is True
    assert order.status == "Cancelled"

def test_view_order_history(customer_controller, session):
    # Seed customer and orders
    customer = Customer(name="Charls", username="charls123", email="charls@123.com", password="password")
    session.add(customer)
    session.commit() 

    # Seed order
    order = Order(customer_id=customer.customer_id, status="Completed", delivery_fee=10.0)
    session.add(order)
    session.commit()

    # Mock messagebox to check output
    with patch("tkinter.messagebox.showinfo") as mock_showinfo:
        customer_controller.view_order_history(session, customer.customer_id)
        mock_showinfo.assert_called_once()

def test_get_customer_profile(customer_controller, session):
    # Seed customer
    customer = Customer(name="Dave", username="dave123", email="dave@example.com", password="password")
    session.add(customer)
    session.commit()

    # Test retrieval of customer profile
    profile = customer_controller.get_customer_profile(session, customer.customer_id)
    assert profile is not None
    assert profile.name == "Dave"
    assert profile.email == "dave@example.com"

def test_make_payment(customer_controller, session, seed_data):
    # Seed customer
    customer_id = seed_data.customer_id

    # Seed order with the generated customer_id
    order = Order(customer_id=customer_id, delivery_option="Delivery", delivery_fee=5.0, status="Completed")
    session.add(order)
    session.commit()

    # Test making a payment
    customer_controller.make_payment(session, order.order_id, "credit_card", 50.0)

    # Refresh session to ensure the latest state
    session.expire_all()

    # Verify the payment record was created as expected
    payment = session.query(Payment).filter_by(order_id=order.order_id).first()
    assert payment is not None, "Payment record was not created."
    assert payment.amount == 50.0, "Payment amount does not match."
    assert payment.payment_type == "credit_card", "Payment type does not match."
    assert payment.payment_status == "completed", "Payment status does not match."



