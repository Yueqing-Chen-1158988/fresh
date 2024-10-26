from tkinter import messagebox

from sqlalchemy import desc, func

from models.customer import Customer
from models.order import Order
from models.order_line import OrderLine
from models.vegetable_premadeBox import Vegetable


def submit_staff_order(self):
    """Submit a new order on behalf of a customer by staff."""
    email = self.customer_email_entry.get()
    vegetable_name = self.staff_vegetable_combobox.get()
    quantity = self.staff_quantity_entry.get()

    customer = self.session.query(Customer).filter_by(email=email).first()
    if not customer:
        messagebox.showerror("Error", "Customer not found.")
        return

    vegetable = self.session.query(Vegetable).filter_by(name=vegetable_name).first()
    if not vegetable:
        messagebox.showerror("Error", "Vegetable not found.")
        return

    # Create a new order for the customer
    new_order = Order(customer_id=customer.customer_id, order_type='vegetable', delivery_option='Collect')
    self.session.add(new_order)
    self.session.commit()

    # Add order line
    order_line = OrderLine(order_id=new_order.order_id, item_name=vegetable.name, quantity=int(quantity), price=vegetable.price_per_unit)
    self.session.add(order_line)
    self.session.commit()

    messagebox.showinfo("Success", f"Order for {quantity} kg of {vegetable_name} placed for {email}.")


def update_order_status(self):
    """Update the status of an existing order."""
    order_id = self.order_id_entry.get()
    new_status = self.status_combobox.get()

    order = self.session.query(Order).filter_by(order_id=order_id).first()
    if not order:
        messagebox.showerror("Error", "Order not found.")
        return

    order.status = new_status
    self.session.commit()
    messagebox.showinfo("Success", f"Order {order_id} status updated to {new_status}.")

def view_customer_details(self):
    """View customer details and order history."""
    search_email = self.customer_search_entry.get()

    customer = self.session.query(Customer).filter_by(email=search_email).first()
    if customer:
        self.customer_details_label.config(text=f"Name: {customer.name}, Email: {customer.email}, Balance: {customer.balance}")
        self.load_customer_order_history(customer.customer_id)
    else:
        messagebox.showerror("Error", "Customer not found.")

def generate_report(self):
    """Generate and display reports based on the selection."""
    report_type = self.report_combobox.get()
    
    if report_type == "Sales":
        # Fetch sales data (e.g., total sales)
        total_sales = self.session.query(func.sum(OrderLine.price * OrderLine.quantity)).scalar()
        messagebox.showinfo("Sales Report", f"Total Sales: ${total_sales:.2f}")

    elif report_type == "Customer List":
        # Fetch customer list
        customers = self.session.query(Customer).all()
        customer_list = "\n".join([f"{c.name} ({c.email})" for c in customers])
        messagebox.showinfo("Customer List", customer_list)

    elif report_type == "Item Popularity":
        # Fetch most popular items
        popular_items = self.session.query(OrderLine.item_name, func.sum(OrderLine.quantity).label('total_quantity'))\
            .group_by(OrderLine.item_name).order_by(desc('total_quantity')).all()
        item_list = "\n".join([f"{item_name}: {quantity} units sold" for item_name, quantity in popular_items])
        messagebox.showinfo("Item Popularity", item_list)


# def update_order_status(self):
#     """Update the status of a selected order."""
#     order_id = self.staff_order_combobox.get()
#     if not order_id:
#         messagebox.showerror("Error", "Please select an order ID.")
#         return

#     # Update order status (this could be a dropdown to select status)
#     order = self.session.query(Order).filter_by(order_id=order_id).first()
#     if order:
#         # Here you can set the new status (this could be from a dropdown in the GUI)
#         order.status = "Processed"  # Update to the desired status
#         self.session.commit()
#         messagebox.showinfo("Success", f"Order {order_id} has been updated to 'Processed'.")
#     else:
#         messagebox.showerror("Error", "Order not found.")
