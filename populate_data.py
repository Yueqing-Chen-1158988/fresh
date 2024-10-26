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

    # Add some initial vegetables
    vegetables = [
        Vegetable(name="Carrot", price_per_unit=0.5, unit="kg"),
        Vegetable(name="Potato", price_per_unit=0.3, unit="kg"),
        Vegetable(name="Tomato", price_per_unit=1.0, unit="pack")
    ]

    # Add some initial premade boxes
    premade_boxes = [
        PremadeBox(size="Small Box", price=10.0),
        PremadeBox(size="Medium Box", price=15.0),
        PremadeBox(size="Large Box", price=20.0)
    ]

   # Add some regular customers
    customers = [
        Customer(name="Jo Ann", username="ann", email="jo@123.com", password="password123", balance=0.0),
        Customer(name="Anna Smith", username="anna", email="anna@123.com", password="password123", balance=10.0)
    ]

    # Add some corporate customers
    corporate_customers = [
        CorporateCustomer(name="TechCorp", username="corp", email="corp@123.com", password="password123", balance=500.0, credit_limit=1000.0, discount_rate=0.15)
    ]

    # Add some staff members
    staff_members = [
        Staff(name="Ella Young", email="ella@123.com", username="ella", password="password123"),
        Staff(name="Dan Brown", email="dan@123.com", username="dan", password="password123")
    ]

    # Add all data to the session
    session.add_all(vegetables + premade_boxes + customers + corporate_customers + staff_members)

    # Commit initial data
    session.commit()

    # Retrieve some customer and product records for order creation
    jo_ann = session.query(Customer).filter_by(name="Jo Ann").first()
    carrot = session.query(Vegetable).filter_by(name="Carrot").first()
    small_box = session.query(PremadeBox).filter_by(size="Small Box").first()

    # Create an order for Jo
    order_jo = Order(
        customer_id=jo_ann.customer_id, 
        order_date=datetime(2024, 10, 24, 9, 10),
        delivery_option="Collect"
    )

    # Add the order to the session and commit to get the order_id
    session.add(order_jo)
    session.commit()  # Commit to generate order_id

    # Add order lines for the order (one for a vegetable, one for a premade box)
    order_line_1 = OrderLine(
        order_id=order_jo.order_id,  # This will be set after the order is added to the session
        item_type="Vegetable",  # Use the enum type defined in the model
        item_name=carrot.name,  # Use the name from the Vegetable model
        quantity=2,
        price=carrot.price_per_unit * 2  # Assuming price is calculated based on quantity
    )
    order_line_2 = OrderLine(
        order_id=order_jo.order_id,  # This will be set after the order is added to the session
        item_type="Premade Box",  # Use the enum type defined in the model
        item_name=small_box.size,  # Use the size as the item name
        quantity=1,
        price=small_box.price  # Direct price from the PremadeBox
    )

    # Create a payment for Jo Ann's order
    payment_jo = Payment(
        order_id=order_jo.order_id,  # This will be set after the order is added to the session
        payment_type="credit_card",  # Use the enum type defined in the model
        payment_status="completed",
        amount=order_line_1.price + order_line_2.price  # Total amount from order lines
    )

    # Add the order and its components to the session
    session.add(order_jo)  # Add the order first
    session.add(order_line_1)
    session.add(order_line_2)
    session.add(payment_jo)

    # Commit the transaction
    session.commit()
    session.close()
    print("Data populated successfully.")

if __name__ == '__main__':
    populate_data()
