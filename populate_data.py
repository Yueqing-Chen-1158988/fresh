from datetime import datetime, timedelta
from database_setup import get_session
from models.customer import Customer, CorporateCustomer
from models.staff import Staff
from models.vegetable_premadeBox import Vegetable, PremadeBox
from models.order import Order
from models.order_line import OrderLine
from models.payment import Payment

def clear_data(session):
    """Clear all existing data from the database tables."""
    session.query(Payment).delete()
    session.query(OrderLine).delete()
    session.query(Order).delete()
    session.query(Customer).delete()
    session.query(CorporateCustomer).delete()
    session.query(Vegetable).delete()
    session.query(PremadeBox).delete()
    session.commit()
    print("Existing data cleared successfully.")

def populate_data():
    session = get_session()
    
    # Clear existing data
    clear_data(session)

    # Add vegetables
    vegetables = [
        Vegetable(name="Carrot", price_per_unit=0.5, unit="kg"),
        Vegetable(name="Potato", price_per_unit=0.3, unit="kg"),
        Vegetable(name="Tomato", price_per_unit=1.0, unit="pack"),
        Vegetable(name="Cucumber", price_per_unit=0.4, unit="kg"),
        Vegetable(name="Lettuce", price_per_unit=0.6, unit="head"),
        Vegetable(name="Broccoli", price_per_unit=1.2, unit="head"),
        Vegetable(name="Bell Pepper", price_per_unit=0.8, unit="kg"),
        Vegetable(name="Spinach", price_per_unit=0.9, unit="pack"),
        Vegetable(name="Onion", price_per_unit=0.5, unit="kg"),
        Vegetable(name="Garlic", price_per_unit=0.2, unit="pack"),
    ]

    # Add premade boxes
    premade_boxes = [
        PremadeBox(size="Small Box", price=10.0),
        PremadeBox(size="Medium Box", price=15.0),
        PremadeBox(size="Large Box", price=20.0)
    ]

    # Add customers
    customers = [
        Customer(name="Jo Ann", username="ann", email="jo@123.com", password="password123", balance=0.0),
        Customer(name="Anna Smith", username="anna", email="anna@123.com", password="password123", balance=10.0),
        Customer(name="Mark Twain", username="mark", email="mark@123.com", password="password123", balance=15.0),
        Customer(name="Lucy Brown", username="lucy", email="lucy@123.com", password="password123", balance=20.0),
        CorporateCustomer(name="TechCorp", username="corp", email="corp@123.com", password="password123", balance=500.0, credit_limit=1000.0, discount_rate=0.1)
    ]

    # Add staff
    staff_members = [
        Staff(name="Ella Young", email="ella@123.com", username="ella", password="password123"),
        Staff(name="Dan Brown", email="dan@123.com", username="dan", password="password123")
    ]

    # Add all data
    session.add_all(vegetables + premade_boxes + customers + staff_members)
    session.commit()

    # Specific orders for each customer
    order_details = [
        {
            "customer": "Jo Ann",
            "items": [("Vegetable", "Carrot", 3), ("Premade Box", "Small Box", 1)],
            "delivery_option": "Collect",
            "payment_type": "credit_card",
            "order_date": datetime(2024, 10, 24, 9, 10),
            "status": "Cancelled"
        },
        {
            "customer": "Anna Smith",
            "items": [("Vegetable", "Potato", 5), ("Vegetable", "Onion", 2)],
            "delivery_option": "Delivery",
            "payment_type": "debit_card",
            "order_date": datetime(2024, 10, 25, 14, 30),
            "status": "Completed"
        },
        {
            "customer": "Mark Twain",
            "items": [("Vegetable", "Broccoli", 1), ("Premade Box", "Medium Box", 1)],
            "delivery_option": "Collect",
            "payment_type": "account",
            "order_date": datetime(2024, 10, 26, 11, 45),
            "status": "Completed"
        },
        {
            "customer": "Lucy Brown",
            "items": [("Vegetable", "Lettuce", 2), ("Vegetable", "Spinach", 3)],
            "delivery_option": "Delivery",
            "payment_type": "credit_card",
            "order_date": datetime(2024, 10, 27, 16, 50),
            "status": "Processing"
        },
        {
            "customer": "TechCorp",
            "items": [("Vegetable", "Bell Pepper", 4), ("Premade Box", "Large Box", 2)],
            "delivery_option": "Delivery",
            "payment_type": "account",
            "order_date": datetime(2024, 10, 28, 13, 20),
            "status": "Processing"
        },
    ]

    # Create orders based on order details
    for details in order_details:
        # Retrieve customer
        customer = session.query(Customer).filter_by(name=details["customer"]).first()
        # Calculate delivery fee based on the delivery option
        delivery_fee = 10.0 if details["delivery_option"] == "Delivery" else 0.0
        
        # Create the order with the calculated delivery fee
        order = Order(
            customer_id=customer.customer_id,
            order_date=details["order_date"],
            delivery_option=details["delivery_option"],
            delivery_fee=delivery_fee,
            status=details["status"]
        )
        session.add(order)
        session.commit()  # Commit here to get the order ID for the order lines

        # Add order lines
        total_amount = 0.0
        for item_type, item_name, quantity in details["items"]:
            if item_type == "Vegetable":
                item = session.query(Vegetable).filter_by(name=item_name).first()
                price = item.price_per_unit * quantity
            else:  # Premade Box
                item = session.query(PremadeBox).filter_by(size=item_name).first()
                price = item.price * quantity

            order_line = OrderLine(
                order_id=order.order_id,
                item_type=item_type,
                item_name=item_name,
                quantity=quantity,
                price=price
            )
            total_amount += price
            session.add(order_line)

        # Add the delivery fee to the total amount
        total_amount += delivery_fee

        # Create payment for the order
        payment = Payment(
            order_id=order.order_id,
            payment_type="credit_card",
            payment_status="completed",
            amount=total_amount
        )
        session.add(payment)
        session.commit()


    # Commit all changes
    session.commit()
    session.close()
    print("Data populated successfully.")

if __name__ == '__main__':
    populate_data()
