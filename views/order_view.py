from tkinter import ttk
import tkinter as tk

class OrderView:
    def __init__(self, root):
        """Open a new window to display the order history."""
        self.root = root
        order_history_window = tk.Toplevel(self.root)
        order_history_window.title("Order History")
        order_history_window.geometry("600x400")

        ttk.Label(order_history_window, text="Your Order History", font=("Arial", 16)).pack(pady=10)

        # Create a Treeview to display order history
        order_history_tree = ttk.Treeview(order_history_window, columns=("Order ID", "Item Name", "Quantity", "Price", "Total Cost"), show="headings")
        order_history_tree.heading("Order ID", text="Order ID")
        order_history_tree.column("Order ID", width=80)

        order_history_tree.heading("Item Name", text="Item Name")
        order_history_tree.column("Item Name", width=150)

        order_history_tree.heading("Quantity", text="Quantity")
        order_history_tree.column("Quantity", width=80)

        order_history_tree.heading("Price", text="Price")
        order_history_tree.column("Price", width=100) 

        order_history_tree.heading("Total Cost", text="Total Cost")
        order_history_tree.column("Total Cost", width=120)

        # Add vertical scrollbar
        scrollbar = ttk.Scrollbar(order_history_window, orient=tk.VERTICAL, command=order_history_tree.yview)
        order_history_tree.configure(yscroll=scrollbar.set)

        # Pack the Treeview and scrollbar
        order_history_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.order_history_tree = order_history_tree
