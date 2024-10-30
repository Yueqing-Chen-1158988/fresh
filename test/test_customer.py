import pytest
from models.customer import Customer, CorporateCustomer

def test_customer_init():
    customer = Customer("John Smith", "john", "john@123.com", "password")
    assert customer.name == "John Smith"
    assert customer.username == "john"
    assert customer.email == "john@123.com"
    assert customer.password_hash != "password"
    assert customer.balance == 0.0

def test_customer_str():
    customer = Customer("John Smith", "john", "john@123.com", "password")
    assert str(customer) == "Customer(John Smith, john@123.com, Balance: 0.0)"

def test_corporate_customer_init():
    corporate_customer = CorporateCustomer("Abc Corp", "abccorp", "abccorp@123.com", "password", 1000.0, 5000.0, 0.1)
    assert corporate_customer.name == "Abc Corp"
    assert corporate_customer.username == "abccorp"
    assert corporate_customer.email == "abccorp@123.com"
    assert corporate_customer.password_hash != "password"
    assert corporate_customer.balance == 1000.0
    assert corporate_customer.credit_limit == 5000.0
    assert corporate_customer.discount_rate == 0.1

def test_corporate_customer_str():
    corporate_customer = CorporateCustomer("Abc Corp", "abccorp", "abccorp@123.com", "password", 1000.0, 5000.0, 0.1)
    assert str(corporate_customer) == "CorporateCustomer(Abc Corp, abccorp@123.com, Balance: 1000.0, Credit Limit: 5000.0, Discount: 0.1)"