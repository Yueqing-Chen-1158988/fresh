import pytest
from models.order_line import OrderLine

@pytest.fixture
def order_line():
    return OrderLine(order_id=1, item_type='Vegetable', item_name='Carrot', quantity=5, price=1.99)

def test_order_line_init(order_line):
    assert order_line.order_id == 1
    assert order_line.item_type == 'Vegetable'
    assert order_line.item_name == 'Carrot'
    assert order_line.quantity == 5
    assert order_line.price == 1.99

def test_order_line_str(order_line):
    expected_output = "OrderLine(Item: Carrot, Quantity: 5, Price: 1.99)"
    assert str(order_line) == expected_output

def test_order_line_relationship(order_line):
    assert order_line.order is None  # Assuming the relationship is not set in this test
