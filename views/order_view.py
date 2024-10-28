from tkinter import Toplevel, ttk, messagebox
import tkinter as tk
from controllers.customer_controller import CustomerController
from models.order import Order
from models.vegetable_premadeBox import Vegetable
from sqlalchemy.orm import joinedload

class OrderView:
    def __init__(self, root, session, user_id):
        """Open a new window to display the order history."""
        self.root = root
        self.session = session
        self.controller = CustomerController(session)
        self.customer_id = user_id

        order_history_window = tk.Toplevel(self.root)
        order_history_window.title("Order History")
        order_history_window.geometry("600x400")

        ttk.Label(order_history_window, text="Your Order History", font=("Arial", 16)).pack(pady=10)

        # Frame to hold both the table and buttons
        content_frame = ttk.Frame(order_history_window)
        content_frame.pack(fill=tk.BOTH, expand=True)

        # Create a Treeview to display order history
        self.order_history_tree = ttk.Treeview(content_frame, columns=("Order ID", "Date", "Total Cost", "Status"), show="headings")
        self.order_history_tree.heading("Order ID", text="Order ID")
        self.order_history_tree.column("Order ID", width=80)
        self.order_history_tree.heading("Date", text="Date")
        self.order_history_tree.column("Date", width=120)
        self.order_history_tree.heading("Total Cost", text="Total Cost")
        self.order_history_tree.column("Total Cost", width=120)
        self.order_history_tree.heading("Status", text="Status")
        self.order_history_tree.column("Status", width=100)
        self.order_history_tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Add a vertical scrollbar for the Treeview
        scrollbar = ttk.Scrollbar(content_frame, orient=tk.VERTICAL, command=self.order_history_tree.yview)
        self.order_history_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Frame for buttons at the bottom of the table
        button_frame = ttk.Frame(content_frame)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

        # Cancel Button
        self.cancel_button = ttk.Button(button_frame, text="Cancel Order", command=self.on_cancel_order)
        self.cancel_button.pack(side=tk.LEFT, padx=10)

        # Order Details Button
        self.details_button = ttk.Button(button_frame, text="Order Details", command=self.on_order_details)
        self.details_button.pack(side=tk.LEFT, padx=10)

        # Load order history
        self.populate_order_history()

    def populate_order_history(self):
        """Populate the order history Treeview with data from the database."""
        # Clear the Treeview
        for row in self.order_history_tree.get_children():
            self.order_history_tree.delete(row)

        # Load data from the controller
        order_data = self.controller.load_order_history(self.session, self.customer_id)
        for order in order_data:
            self.order_history_tree.insert("", "end", values=order)

    def on_cancel_order(self):
        """Handle the cancel order button click."""
        selected_item = self.order_history_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select an order to cancel.")
            return

        order_id = self.order_history_tree.item(selected_item)['values'][0]
        if self.controller.cancel_order(self.session, order_id):
            messagebox.showinfo("Success", "Order has been cancelled.")
            self.populate_order_history()  # Refresh the view
        else:
            messagebox.showerror("Error", "Order cannot be cancelled.")

    def on_order_details(self):
        """Handle the order details button click."""
        selected_item = self.order_history_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select an order to view details.")
            return

        order_id = self.order_history_tree.item(selected_item)['values'][0]
        # Add logic here to display order details
        self.view_order_detail(order_id)

    def view_order_detail(self, order_id):
        """Display detailed information for a specific order, including order lines."""
        order_detail = self.get_order_detail(order_id)
        if not order_detail:
            messagebox.showerror("Error", "Unable to retrieve order details.")
            return
        
        # Create a new window to display the order details
        detail_window = Toplevel(self.root)
        detail_window.title(f"Order Details - ID: {order_id}")
        detail_window.geometry("700x500")

        # Delivery option and fee
        ttk.Label(detail_window, text=f"Delivery Option: {order_detail['delivery_option']}").pack(anchor=tk.W, padx=10, pady=5)
        ttk.Label(detail_window, text=f"Delivery Fee: ${order_detail['delivery_fee']:.2f}").pack(anchor=tk.W, padx=10, pady=5)

        # Total cost
        ttk.Label(detail_window, text=f"Total Cost: ${order_detail['total_cost']:.2f}", font=("Arial", 12, "bold")).pack(anchor=tk.W, padx=10, pady=10)

        # Separate frame for each item type
        veg_frame = ttk.LabelFrame(detail_window, text="Vegetable Items")
        veg_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        box_frame = ttk.LabelFrame(detail_window, text="Premade Box Items")
        box_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Vegetable Items Treeview
        veg_tree = ttk.Treeview(veg_frame, columns=("Item", "Quantity", "Unit", "Price"), show="headings")
        veg_tree.heading("Item", text="Item")
        veg_tree.heading("Quantity", text="Quantity")
        veg_tree.heading("Unit", text="Unit")
        veg_tree.heading("Price", text="Price")
        veg_tree.pack(fill=tk.BOTH, expand=True)

        # Premade Box Items Treeview
        box_tree = ttk.Treeview(box_frame, columns=("Size", "Quantity", "Price"), show="headings")
        box_tree.heading("Size", text="Size")
        box_tree.heading("Quantity", text="Quantity")
        box_tree.heading("Price", text="Price")
        box_tree.pack(fill=tk.BOTH, expand=True)

        # Populate Treeviews with Order Lines data
        for line in order_detail['order_lines']:
            if line['item_type'] == 'Vegetable':
                veg_tree.insert("", "end", values=(line['item_name'], line['quantity'], line['unit'], f"${line['subtotal']:.2f}"))
            elif line['item_type'] == 'Premade Box':
                box_tree.insert("", "end", values=(line['item_name'], line['quantity'], f"${line['subtotal']:.2f}"))

        detail_window.transient(self.root)
        detail_window.grab_set()
        self.root.wait_window(detail_window)

    def open_order_history(self, root, session, user_id):
        orderview = OrderView(root, session, user_id)
        self.controller.load_order_history(session, orderview.order_history_tree)

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