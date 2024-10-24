from tkinter import messagebox
from models.order import Order
from models.order_line import OrderLine
from models.vegetable_premadeBox import PremadeBox, Vegetable
from views.order_view import OrderView

def get_vegetable_names(session):
    """Fetch vegetable names from the database."""
    vegetables = session.query(Vegetable).all()
    return [veg.name for veg in vegetables]

def get_premade_box_sizes(session):
    """Fetch premade box sizes from the database."""
    boxes = session.query(PremadeBox).all()
    return [box.size for box in boxes]

def update_vegetable_info(event, session, vegetable_combobox, price_label, unit_label):
    """Update the price and unit labels based on the selected vegetable."""
    vegetable_name = vegetable_combobox.get()
    vegetable = session.query(Vegetable).filter_by(name=vegetable_name).first()
    print("update_vegetable_info >>>")
    print(vegetable)
    
    if vegetable:
        price_label.config(text=f"${vegetable.price_per_unit:.2f}")
        unit_label.config(text=vegetable.unit)  # Assuming you have a unit attribute in your Vegetable model
    else:
        price_label.config(text="")
        unit_label.config(text="")

def submit_order(session, root, vegetable_combobox, quantity_entry):
    """Submit a new order along with its order line."""
    vegetable_name = vegetable_combobox.get()
    quantity = quantity_entry.get()

    if not vegetable_name or not quantity.isdigit() or int(quantity) <= 0:
        messagebox.showerror("Error", "Please select a vegetable and enter a valid positive quantity.")
        return

    # Fetch vegetable from the database
    vegetable = session.query(Vegetable).filter_by(name=vegetable_name).first()
    if vegetable:
        # Create a new order
        new_order = Order(customer_id=1, order_type='vegetable', delivery_option='collect')  # Placeholder customer_id
        session.add(new_order)
        session.commit()  # Commit to get the new order ID

        # Create an order line for the newly created order
        order_line = OrderLine(order_id=new_order.order_id, item_name=vegetable.name, quantity=int(quantity), price=vegetable.price_per_unit)
        session.add(order_line)
        session.commit()

        messagebox.showinfo("Success", f"Order for {quantity} kg of {vegetable_name} has been placed.")
    else:
        messagebox.showerror("Error", "Vegetable not found.")

def submit_premade_box_order(session, premade_box_combobox, box_quantity_entry):
    """Submit a new order for a premade box."""
    box_name = premade_box_combobox.get()
    quantity = box_quantity_entry.get()

    if not box_name or not quantity.isdigit() or int(quantity) <= 0:
        messagebox.showerror("Error", "Please select a premade box and enter a valid positive quantity.")
        return

    # Fetch premade box from the database
    premade_box = session.query(PremadeBox).filter_by(size=box_name).first()
    if premade_box:
        # Create a new order
        new_order = Order(customer_id=1, order_type='premade_box', delivery_option='collect')  # Placeholder customer_id
        session.add(new_order)
        session.commit()  # Commit to get the new order ID

        # Create an order line for the premade box
        order_line = OrderLine(order_id=new_order.order_id, item_name=premade_box.size, quantity=int(quantity), price=premade_box.price)
        session.add(order_line)
        session.commit()

        messagebox.showinfo("Success", f"Order for {quantity} {box_name} box has been placed.")
    else:
        messagebox.showerror("Error", "Premade box not found.")
                
def open_order_history(session, root):
    orderview = OrderView(root)
    load_order_history(session, orderview.order_history_tree)
    

def load_order_history(session, order_history_tree):
    """Load the customer's order history into the treeview."""
    for row in order_history_tree.get_children():
        order_history_tree.delete(row)

    # Fetch orders for a specific customer from the database
    orders = session.query(Order).filter_by(customer_id=1).all()  # Placeholder customer_id
    for order in orders:
        order_lines = session.query(OrderLine).filter_by(order_id=order.order_id).all()
        total_cost = sum(line.quantity * line.price for line in order_lines)  # Calculate total cost

        for line in order_lines:
            order_history_tree.insert("", "end", values=(order.order_id, line.item_name, line.quantity, f"${line.price:.2f}", f"${total_cost:.2f}"))