import pytest
from models.order import Order

@pytest.fixture
def test_order_creation():
    order = Order(customer_id=1, delivery_option='Delivery', delivery_fee=5.0, staff_id=2, status='Processing')
    assert order.customer_id == 1
    assert order.delivery_option == 'Delivery'
    assert order.delivery_fee == 5.0
    assert order.staff_id == 2
    assert order.status == 'Processing'

def test_order_cancelation():
    order = Order(customer_id=1)
    assert order.status == 'Processing'
    order.cancel_order()
    assert order.status == 'Cancelled'