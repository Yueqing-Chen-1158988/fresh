from tkinter import messagebox
from models.order import Order
from models.order_line import OrderLine
from models.vegetable_premadeBox import PremadeBox, Vegetable


def submit_order(session, customer_id, vegetable_combobox, quantity_entry, delivery_combobox, delivery_fee_label):
    """Submit a new order along with its order line and delivery details."""
    vegetable_name = vegetable_combobox.get()
    quantity = quantity_entry.get()
    delivery_option = delivery_combobox.get()
    delivery_fee = float(delivery_fee_label.cget("text").strip("$"))

    if not vegetable_name or not quantity.isdigit() or int(quantity) <= 0:
        messagebox.showerror("Error", "Please select a vegetable and enter a valid positive quantity.")
        return

    try:
        # Fetch vegetable from the database
        vegetable = session.query(Vegetable).filter_by(name=vegetable_name).first()

        if vegetable:
            # Create a new order
            new_order = Order(customer_id=customer_id, order_type='vegetable', delivery_option=delivery_option, delivery_fee=delivery_fee)
            print("new_order >>>")
            session.add(new_order)
            session.commit()  # Commit to get the new order ID

            # Create an order line for the newly created order
            order_line = OrderLine(order_id=new_order.order_id, item_name=vegetable.name, quantity=int(quantity), price=vegetable.price_per_unit)
            session.add(order_line)
            session.commit()

            messagebox.showinfo("Success", f"Order for {quantity} kg of {vegetable_name} has been placed with {delivery_option}.")
        else:
            messagebox.showerror("Error", "Vegetable not found.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


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

def load_order_history(session, customer_id):
    """Fetch order history for a specific customer."""
    # Fetch orders for the customer from the database
    orders = session.query(Order).filter_by(customer_id=customer_id).all()
    order_data = []
    for order in orders:
        order_lines = session.query(OrderLine).filter_by(order_id=order.order_id).all()
        total_cost = sum(line.quantity * line.price for line in order_lines)
        for line in order_lines:
            order_data.append((order.order_id, line.item_name, line.quantity, f"${line.price:.2f}", f"${total_cost:.2f}", order.status))
    return order_data

def cancel_order(session, order_id):
    """Cancel an order if it is in 'Processing' status."""
    order = session.query(Order).filter_by(order_id=order_id).first()
    if order and order.status == "Processing":
        order.status = "Cancelled"
        session.commit()
        return True  # Indicate that the cancellation was successful
    else:
        return False  # Indicate that the order could not be cancelled
