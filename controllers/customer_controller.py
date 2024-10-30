from tkinter import messagebox
from models.customer import Customer
from models.order import Order
from models.order_line import OrderLine
from models.payment import Payment
from models.vegetable_premadeBox import PremadeBox, Vegetable

class CustomerController:
    def __init__(self, session):
        self.session = session

    def get_vegetable_names(self, session):
        """Fetch vegetable names from the database."""
        vegetables = session.query(Vegetable).all()
        return [veg.name for veg in vegetables]

    def get_premade_box_sizes(self, session):
        """Fetch premade box sizes from the database."""
        boxes = session.query(PremadeBox).all()
        return [box.size for box in boxes]

    def update_vegetable_info(self, event, session, vegetable_combobox, price_label, unit_label):
        """Update the price and unit labels based on the selected vegetable."""
        vegetable_name = vegetable_combobox.get()
        vegetable = session.query(Vegetable).filter_by(name=vegetable_name).first()
        
        if vegetable:
            price_label.config(text=f"${vegetable.price_per_unit:.2f}")
            unit_label.config(text=vegetable.unit)
        else:
            price_label.config(text="")
            unit_label.config(text="")

    def add_item_to_cart(self, cart, item_type, item_name, quantity, price_per_unit):
        """Add an item to the cart with subtotal after validation."""
        # Validate inputs
        if not item_type or not item_name or not quantity or not price_per_unit:
            messagebox.showerror("Error", "Please select an item type, item, and enter a quantity.")
            return None

        try:
            quantity = int(quantity)
            if quantity <= 0:
                raise ValueError("Quantity must be positive")
        except ValueError:
            messagebox.showerror("Error", "Quantity must be a positive integer.")
            return None

        try:
            price = float(price_per_unit)
            if price <= 0:
                raise ValueError("Price must be positive")
        except ValueError:
            messagebox.showerror("Error", "Invalid price value.")
            return None

        # Calculate subtotal and create cart item
        subtotal = quantity * price
        cart_item = {
            "type": item_type,
            "name": item_name,
            "quantity": quantity,
            "price": price,
            "subtotal": subtotal
        }

        # Add to cart and return updated item
        cart.append(cart_item)
        return cart_item
    
    def calculate_cart_totals(self, cart):
        """Calculate and return the total cost of items in the cart."""
        total_cost = sum(item["subtotal"] for item in cart)
        return total_cost

    def submit_order(self, session, customer_id, cart, delivery_option, delivery_fee):
        """Submit an order with all items in the cart and delivery details."""
        if not cart:
            messagebox.showerror("Error", "The cart is empty. Add items before submitting.")
            return
        
        if not delivery_option:
            messagebox.showerror("Error", "Please select a delivery option before submitting.")
            return
        
        try:
            # Create a new order
            new_order = Order(customer_id=customer_id, delivery_option=delivery_option, delivery_fee=delivery_fee)
            session.add(new_order)
            session.commit()

            # Create order lines for each item in the cart
            for item in cart:
                order_line = OrderLine(
                    order_id=new_order.order_id,
                    item_type=item["type"],
                    item_name=item["name"],
                    quantity=item["quantity"],
                    price=item["price"]
                )
                session.add(order_line)

            session.commit()
            messagebox.showinfo("Success", "Order has been successfully placed.")
            return new_order.order_id  # Return the order ID for reference
        except Exception as e:
            session.rollback()
            messagebox.showerror("Error", f"An error occurred: {e}")
            return None

    def load_order_history(self, session, customer_id):
        """Fetch order history for a specific customer."""
        orders = session.query(Order).filter_by(customer_id=customer_id).all()
        order_data = []
        for order in orders:
            order_lines = session.query(OrderLine).filter_by(order_id=order.order_id).all()
            total_cost = sum(line.quantity * line.price for line in order_lines) + order.delivery_fee

            # Format order_date to DD/MM/YYYY format for New Zealand
            formatted_date = order.order_date.strftime("%d/%m/%Y")

            order_data.append((order.order_id, formatted_date, f"${total_cost:.2f}", order.status))
        return order_data

    def cancel_order(self, session, order_id):
        """Cancel an order if it is in 'Processing' status."""
        order = session.query(Order).filter_by(order_id=order_id).first()
        if order and order.status == "Processing":
            order.status = "Cancelled"
            session.commit()
            return True
        else:
            return False
    def view_order_history(self, session, customer_id):
        """Retrieve and display the order history for a customer."""
        order_data = self.load_order_history(session, customer_id)
        
        # Display the order history in a readable format
        if order_data:
            history_text = "Order History:\n\n"
            for order_id, order_date, total_cost, status in order_data:
                history_text += (f"Order ID: {order_id}\n"
                                f"Date: {order_date}\n"
                                f"Total Cost: {total_cost}\n"
                                f"Status: {status}\n\n")
            messagebox.showinfo("Order History", history_text)
        else:
            messagebox.showinfo("Order History", "No orders found.")                

    def get_customer_profile(self, session, customer_id):
        """Fetch customer profile details by ID."""
        return session.query(Customer).filter_by(customer_id=customer_id).first()

    def make_payment(self, session, order_id, payment_type, amount):
        """Process a payment for the specified order."""
        try:
            # Insert payment record
            new_payment = Payment(
                order_id=order_id,
                payment_type=payment_type,
                amount=amount,
                payment_status="completed"
            )
            session.add(new_payment)
            session.commit()
            messagebox.showinfo("Success", "Payment completed successfully.")
        except Exception as e:
            session.rollback()
            messagebox.showerror("Error", f"Payment failed: {e}")