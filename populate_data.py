from datetime import datetime
from database_setup import get_session
from models.base import Base
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
        Customer(name="Anna Smith", username="anna", email="anna@123.com", password="password123", balance=10.0)
    ]

    # Add some corporate customers
    corporate_customers = [
        CorporateCustomer(name="TechCorp", username="corp", email="corp@123.com", password="password123", balance=500.0, credit_limit=1000.0, discount_rate=0.15)
    ]

    # Add staff
    staff_members = [
        Staff(name="Ella Young", email="ella@123.com", username="ella", password="password123"),
        Staff(name="Dan Brown", email="dan@123.com", username="dan", password="password123")
    ]

    # Add all data
    session.add_all(vegetables + premade_boxes + customers + corporate_customers + staff_members)
    session.commit()

    # Retrieve customer and product for order creation
    jo_ann = session.query(Customer).filter_by(name="Jo Ann").first()
    carrot = session.query(Vegetable).filter_by(name="Carrot").first()
    small_box = session.query(PremadeBox).filter_by(size="Small Box").first()

    # Create an order for Jo
    order_jo = Order(
        customer_id=jo_ann.customer_id, 
        order_date=datetime(2024, 10, 24, 9, 10),
        delivery_option="Collect"
    )

    # Add the order
    session.add(order_jo)
    session.commit()

    # Add order lines for the order
    order_line_1 = OrderLine(
        order_id=order_jo.order_id, 
        item_type="Vegetable",
        item_name=carrot.name,
        quantity=2,
        price=carrot.price_per_unit * 2
    )
    order_line_2 = OrderLine(
        order_id=order_jo.order_id, 
        item_type="Premade Box",
        item_name=small_box.size,
        quantity=1,
        price=small_box.price
    )

    # Create a payment for Jo Ann's order
    payment_jo = Payment(
        order_id=order_jo.order_id,
        payment_type="credit_card", 
        payment_status="completed",
        amount=order_line_1.price + order_line_2.price 
    )

    # Add the order and its components to the session
    session.add(order_jo)
    session.add(order_line_1)
    session.add(order_line_2)
    session.add(payment_jo)

    # Commit the transaction
    session.commit()
    session.close()
    print("Data populated successfully.")

if __name__ == '__main__':
    populate_data()
