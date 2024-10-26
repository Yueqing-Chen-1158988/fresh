from tkinter import ttk, messagebox
import tkinter as tk
from controllers.customer_controller import load_order_history, cancel_order

class OrderView:
    def __init__(self, root, session, user_id):
        """Open a new window to display the order history."""
        self.root = root
        self.session = session
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
        order_data = load_order_history(self.session, self.customer_id)
        for order in order_data:
            self.order_history_tree.insert("", "end", values=order)

    def on_cancel_order(self):
        """Handle the cancel order button click."""
        selected_item = self.order_history_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select an order to cancel.")
            return

        order_id = self.order_history_tree.item(selected_item)['values'][0]
        if cancel_order(self.session, order_id):
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
        messagebox.showinfo("Order Details", f"Details for Order ID: {order_id}")

    def open_order_history(root, session, user_id):
        orderview = OrderView(root, session, user_id)
        load_order_history(session, orderview.order_history_tree)
