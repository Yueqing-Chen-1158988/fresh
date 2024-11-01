import pytest
from models.payment import Payment

@pytest.fixture
def test_payment_init():
    payment = Payment(order_id=1, payment_type='credit_card', payment_status='pending', amount=100.0)
    assert payment.order_id == 1
    assert payment.payment_type == 'credit_card'
    assert payment.payment_status == 'pending'
    assert payment.amount == 100.0

def test_payment_str():
    payment = Payment(order_id=1, payment_type='credit_card', payment_status='pending', amount=100.0)
    expected_output = "Payment(Order: 1, Type: credit_card, Status: pending, Amount: 100.0)"
    assert str(payment) == expected_output
