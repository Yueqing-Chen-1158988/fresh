from models.vegetable_premadeBox import Vegetable, PremadeBox
from models.order import Order
from models.order_line import OrderLine
from models.customer import Customer
from datetime import datetime, timedelta
from sqlalchemy import func

class StaffController:
    def __init__(self, session):
        self.session = session

    def get_all_items(self):
        vegetables = self.session.query(Vegetable).all()
        premade_boxes = self.session.query(PremadeBox).all()
        items_text = "Vegetables:\n" + "\n".join(f"- {veg.name}, {veg.unit}: ${veg.price_per_unit}" for veg in vegetables)
        items_text += "\n\nPremade Boxes:\n" + "\n".join(f"- {box.size}: ${box.price}" for box in premade_boxes)
        return items_text

    def get_orders_by_type(self, order_type):
        if order_type == "Current Orders":
            orders = self.session.query(Order).filter(Order.status == "Processing").all()
        elif order_type == "Previous Orders":
            orders = self.session.query(Order).filter(Order.status != "Processing").all()
        else:
            return None
        return "\n".join(f"Order ID: {order.order_id}, Date: {order.order_date}, Status: {order.status}, Total: ${self.get_order_total(order)}" for order in orders)

    def get_order_total(self, order):
        return sum(line.quantity * line.price for line in order.order_lines) + order.delivery_fee

    def update_order_status(self, order_id, new_status):
        order = self.session.query(Order).filter_by(order_id=order_id).first()
        if order:
            order.status = new_status
            self.session.commit()
            return True
        return False

    def get_customer_details(self, email):
        customer = self.session.query(Customer).filter_by(email=email).first()
        if customer:
            return f"Name: {customer.name}\nEmail: {customer.email}\nBalance: ${customer.balance}\nAddress: {customer.address}"
        return None

    def get_customer_list(self):
        customers = self.session.query(Customer).all()
        return "\n".join(f"{cust.name} ({cust.email})" for cust in customers)

    def generate_sales_report(self, timeframe):
        today = datetime.today()
        start_date = today - {"Weekly Sales": timedelta(days=7), "Monthly Sales": timedelta(days=30), "Yearly Sales": timedelta(days=365)}.get(timeframe, timedelta(days=0))
        if start_date == timedelta(days=0):
            return None
        sales = self.session.query(Order).filter(Order.order_date >= start_date).all()
        total_sales = sum(self.get_order_total(order) for order in sales)
        return f"Total Sales: ${total_sales:.2f}"

    def get_popular_items(self):
        popular_items = self.session.query(OrderLine.item_name, func.count(OrderLine.item_name))\
                                     .group_by(OrderLine.item_name)\
                                     .order_by(func.count(OrderLine.item_name).desc()).limit(5).all()
        return "Most Popular Items:\n" + "\n".join(f"{item} - Ordered {count} times" for item, count in popular_items)
