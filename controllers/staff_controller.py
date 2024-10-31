from models.vegetable_premadeBox import Vegetable, PremadeBox
from models.order import Order
from models.order_line import OrderLine
from models.customer import CorporateCustomer, Customer
from datetime import datetime, timedelta
from sqlalchemy import func
from sqlalchemy.orm import joinedload

class StaffController:
    def __init__(self, session):
        self.session = session

    def get_all_vegetables(self):
        """Fetch all vegetables from the database."""
        vegetables = self.session.query(Vegetable).all()
        return vegetables 
    
    def get_all_premade_boxes(self):
        """Fetch all premade boxes from the database."""
        premade_boxes = self.session.query(PremadeBox).all()
        return premade_boxes

    def get_orders_by_type(self, order_type):
        """Fetch orders based on the order type."""
        if order_type == "Current Orders":
            orders = self.session.query(Order).filter(Order.status == "Processing").all()
        elif order_type == "Previous Orders":
            orders = self.session.query(Order).filter(Order.status != "Processing").all()
        else:
            return []  # Return an empty list if the order type is not recognized
        return orders 
    
    def get_order_total(self, order):
        """Calculate the total cost of an order."""
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

        # Get order line details
        for line in order.order_lines:
            item_data = {
                "item_type": line.item_type,
                "item_name": line.item_name,
                "quantity": line.quantity,
                "price": line.price,
                "subtotal": line.quantity * line.price
            }
            
            if line.item_type == 'Vegetable':
                # Get the unit of the vegetable
                vegetable = self.session.query(Vegetable).filter(Vegetable.name == line.item_name).first()
                item_data["unit"] = vegetable.unit if vegetable else "Unknown"
            else:
                # Premade boxes do not need units
                item_data["unit"] = "N/A"
            
            order_detail["order_lines"].append(item_data)

        return order_detail
    
    def update_order_status(self, order_id, new_status):
        """Update the status of an order."""
        order = self.session.query(Order).filter_by(order_id=order_id).first()
        if order:
            order.status = new_status
            self.session.commit()
            return True
        return False

    def get_all_customers(self):
        """Retrieve all customers from the database."""
        # Retrieve regular customers
        regular_customers = self.session.query(Customer).filter(~Customer.customer_id.in_(
            self.session.query(CorporateCustomer.customer_id)
        )).all()
    
        # Retrieve corporate customers
        corporate_customers = self.session.query(CorporateCustomer).all()

        # Combine lists, corporate customers have credit_limit while regular ones do not
        return regular_customers + corporate_customers

    def get_customers_by_name(self, name):
        """Retrieve customers whose names match the search input."""
        return self.session.query(Customer).filter(Customer.name.ilike(f"%{name}%")).all()
    
    def generate_sales_report(self, timeframe):
        """Generate sales report data for the specified timeframe."""
        now = datetime.now()
        
        # Determine the start date based on the selected timeframe
        if timeframe == "Week":
            start_date = now - timedelta(days=7)
        elif timeframe == "Month":
            start_date = now.replace(day=1)
        elif timeframe == "Year":
            start_date = now.replace(month=1, day=1)
        else:
            return []

        # Calculate daily total sales
        daily_sales_data = self.session.query(
            func.date(Order.order_date).label("order_date"),
            (func.sum(OrderLine.quantity * OrderLine.price) + func.sum(Order.delivery_fee)).label("total_sales")
        ).join(OrderLine).filter(Order.order_date >= start_date) \
         .group_by(func.date(Order.order_date)).all()
        
        daily_sales = [(str(order_date), round(total_sales, 2)) for order_date, total_sales in daily_sales_data]
        total_sales_in_timeframe = sum(total for _, total in daily_sales)
        daily_sales.append(("Total Sales", round(total_sales_in_timeframe, 2)))

        return daily_sales
    
    def get_popular_items(self):
        """Fetch the most popular items based on the number of times they have been ordered."""
        popular_items = self.session.query(OrderLine.item_name, func.count(OrderLine.item_name))\
                                    .group_by(OrderLine.item_name)\
                                    .order_by(func.count(OrderLine.item_name).desc()).limit(5).all()
        return [(item, count) for item, count in popular_items]
