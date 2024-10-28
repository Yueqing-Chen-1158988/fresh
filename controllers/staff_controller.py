from models.vegetable_premadeBox import Vegetable, PremadeBox
from models.order import Order
from models.order_line import OrderLine
from models.customer import Customer
from datetime import datetime, timedelta
from sqlalchemy import func
from sqlalchemy.orm import joinedload

class StaffController:
    def __init__(self, session):
        self.session = session

    def get_all_vegetables(self):
        """Fetch all vegetables from the database."""
        vegetables = self.session.query(Vegetable).all()
        return vegetables  # Return a list of Vegetable objects
    
    def get_all_premade_boxes(self):
        """Fetch all premade boxes from the database."""
        premade_boxes = self.session.query(PremadeBox).all()
        return premade_boxes  # Return a list of PremadeBox objects

    def get_orders_by_type(self, order_type):
        if order_type == "Current Orders":
            orders = self.session.query(Order).filter(Order.status == "Processing").all()
        elif order_type == "Previous Orders":
            orders = self.session.query(Order).filter(Order.status != "Processing").all()
        else:
            return []  # Return an empty list if the order type is not recognized
        return orders  # Return the list of orders

    def get_order_total(self, order):
        return sum(line.quantity * line.price for line in order.order_lines) + order.delivery_fee

    def get_order_detail(self, order_id):
        """Fetch detailed order information, including order lines, delivery fee, and total cost."""
        order = self.session.query(Order).options(joinedload(Order.order_lines)).filter(Order.order_id == order_id).first()
        if not order:
            return None

        order_detail = {
            "delivery_option": order.delivery_option,
            "delivery_fee": order.delivery_fee,
            "total_cost": sum(line.quantity * line.price for line in order.order_lines) + order.delivery_fee,
            "order_lines": []
        }

        # Collect order line details
        for line in order.order_lines:
            item_data = {
                "item_type": line.item_type,
                "item_name": line.item_name,
                "quantity": line.quantity,
                "price": line.price,
                "subtotal": line.quantity * line.price
            }
            
            if line.item_type == 'Vegetable':
                # Get the unit of the vegetable (assuming price includes unit)
                vegetable = self.session.query(Vegetable).filter(Vegetable.name == line.item_name).first()
                item_data["unit"] = vegetable.unit if vegetable else "Unknown"
            else:
                # Premade boxes do not need units
                item_data["unit"] = "N/A"
            
            order_detail["order_lines"].append(item_data)

        return order_detail
    
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
