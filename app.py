import tkinter as tk
from tkinter import ttk, messagebox
from sqlalchemy.orm import sessionmaker
from database_setup import get_session
from models.customer import Customer, CorporateCustomer
from models.order import Order
from models.order_line import OrderLine
from models.payment import Payment
from models.vegetable_premadeBox import Vegetable, PremadeBox

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Vegetable Ordering System")
        self.root.geometry("800x800")

        self.session = get_session()  # Initialize database session

        # Create a main frame
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Create a notebook (tabbed interface)
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Create tabs
        self.customer_tab = ttk.Frame(self.notebook)
        self.staff_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.customer_tab, text="Customer")
        self.notebook.add(self.staff_tab, text="Staff")

        # Initialize customer functionalities
        self.init_customer_functions()
        
        # Initialize staff functionalities
        self.init_staff_functions()

    def init_customer_functions(self):
        """Initialize customer functionalities."""
        # Place Order Section
        ttk.Label(self.customer_tab, text="Place an Order", font=("Arial", 16)).pack(pady=10)

        self.order_frame = ttk.LabelFrame(self.customer_tab, text="Order Form")
        self.order_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Vegetable Selection Section
        ttk.Label(self.order_frame, text="Select Vegetable:").grid(row=0, column=0, padx=5, pady=5)
        self.vegetable_combobox = ttk.Combobox(self.order_frame, values=self.get_vegetable_names())
        self.vegetable_combobox.grid(row=0, column=1, padx=5, pady=5)
        self.vegetable_combobox.bind("<<ComboboxSelected>>", self.update_vegetable_info)

        # Labels for price and unit
        ttk.Label(self.order_frame, text="Price per Unit:").grid(row=1, column=0, padx=5, pady=5)
        self.price_label = ttk.Label(self.order_frame, text="")
        self.price_label.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.order_frame, text="Unit:").grid(row=2, column=0, padx=5, pady=5)
        self.unit_label = ttk.Label(self.order_frame, text="")
        self.unit_label.grid(row=2, column=1, padx=5, pady=5)

        # Quantity Entry
        ttk.Label(self.order_frame, text="Quantity:").grid(row=3, column=0, padx=5, pady=5)
        self.quantity_entry = ttk.Entry(self.order_frame)
        self.quantity_entry.grid(row=3, column=1, padx=5, pady=5)

        # Submit Order Button
        self.submit_order_button = ttk.Button(self.order_frame, text="Submit Order", command=self.submit_order)
        self.submit_order_button.grid(row=4, columnspan=2, pady=10)


        # View Order History Button
        self.view_order_history_button = ttk.Button(self.order_frame, text="View Order History", command=self.open_order_history)
        self.view_order_history_button.grid(row=5, columnspan=2, pady=10)


        # Premade Box Order Section
        ttk.Label(self.customer_tab, text="Order Premade Box", font=("Arial", 16)).pack(pady=10)

        self.box_frame = ttk.LabelFrame(self.customer_tab, text="Premade Box Order Form")
        self.box_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Premade Box Selection
        ttk.Label(self.box_frame, text="Select Premade Box:").grid(row=0, column=0, padx=5, pady=5)
        self.premade_box_combobox = ttk.Combobox(self.box_frame, values=self.get_premade_box_sizes())
        self.premade_box_combobox.grid(row=0, column=1, padx=5, pady=5)

        # Box Quantity Entry
        ttk.Label(self.box_frame, text="Quantity:").grid(row=1, column=0, padx=5, pady=5)
        self.box_quantity_entry = ttk.Entry(self.box_frame)
        self.box_quantity_entry.grid(row=1, column=1, padx=5, pady=5)

        # Submit Box Order Button
        self.submit_box_order_button = ttk.Button(self.box_frame, text="Submit Box Order", command=self.submit_premade_box_order)
        self.submit_box_order_button.grid(row=2, columnspan=2, pady=10)

    def init_staff_functions(self):
        """Initialize staff functionalities."""
        # Staff Order Section
        ttk.Label(self.staff_tab, text="Process Customer Orders", font=("Arial", 16)).pack(pady=10)

        self.staff_order_frame = ttk.LabelFrame(self.staff_tab, text="Order Processing")
        self.staff_order_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Order Selection for Staff
        ttk.Label(self.staff_order_frame, text="Select Order ID:").grid(row=0, column=0, padx=5, pady=5)
        self.staff_order_combobox = ttk.Combobox(self.staff_order_frame, values=self.get_order_ids())
        self.staff_order_combobox.grid(row=0, column=1, padx=5, pady=5)

        # Update Order Status Button
        self.update_order_status_button = ttk.Button(self.staff_order_frame, text="Update Order Status", command=self.update_order_status)
        self.update_order_status_button.grid(row=1, columnspan=2, pady=10)

    def get_vegetable_names(self):
        """Fetch vegetable names from the database."""
        vegetables = self.session.query(Vegetable).all()
        return [veg.name for veg in vegetables]

    def get_premade_box_sizes(self):
        """Fetch premade box sizes from the database."""
        boxes = self.session.query(PremadeBox).all()
        return [box.size for box in boxes]

    def update_vegetable_info(self, event):
        """Update the price and unit labels based on the selected vegetable."""
        vegetable_name = self.vegetable_combobox.get()
        vegetable = self.session.query(Vegetable).filter_by(name=vegetable_name).first()
        
        if vegetable:
            self.price_label.config(text=f"${vegetable.price_per_unit:.2f}")
            self.unit_label.config(text=vegetable.unit)  # Assuming you have a unit attribute in your Vegetable model
        else:
            self.price_label.config(text="")
            self.unit_label.config(text="")

    def get_order_ids(self):
        """Fetch order IDs from the database for staff processing."""
        orders = self.session.query(Order).all()
        return [order.order_id for order in orders]

    def submit_order(self):
        """Submit a new order along with its order line."""
        vegetable_name = self.vegetable_combobox.get()
        quantity = self.quantity_entry.get()

        if not vegetable_name or not quantity.isdigit() or int(quantity) <= 0:
            messagebox.showerror("Error", "Please select a vegetable and enter a valid positive quantity.")
            return

        # Fetch vegetable from the database
        vegetable = self.session.query(Vegetable).filter_by(name=vegetable_name).first()
        if vegetable:
            # Create a new order
            new_order = Order(customer_id=1, order_type='vegetable', delivery_option='collect')  # Placeholder customer_id
            self.session.add(new_order)
            self.session.commit()  # Commit to get the new order ID

            # Create an order line for the newly created order
            order_line = OrderLine(order_id=new_order.order_id, item_name=vegetable.name, quantity=int(quantity), price=vegetable.price_per_unit)
            self.session.add(order_line)
            self.session.commit()

            messagebox.showinfo("Success", f"Order for {quantity} kg of {vegetable_name} has been placed.")
            self.load_order_history()
        else:
            messagebox.showerror("Error", "Vegetable not found.")

    def submit_premade_box_order(self):
        """Submit a new order for a premade box."""
        box_name = self.premade_box_combobox.get()
        quantity = self.box_quantity_entry.get()

        if not box_name or not quantity.isdigit() or int(quantity) <= 0:
            messagebox.showerror("Error", "Please select a premade box and enter a valid positive quantity.")
            return

        # Fetch premade box from the database
        premade_box = self.session.query(PremadeBox).filter_by(size=box_name).first()
        if premade_box:
            # Create a new order
            new_order = Order(customer_id=1, order_type='premade_box', delivery_option='collect')  # Placeholder customer_id
            self.session.add(new_order)
            self.session.commit()  # Commit to get the new order ID

            # Create an order line for the premade box
            order_line = OrderLine(order_id=new_order.order_id, item_name=premade_box.size, quantity=int(quantity), price=premade_box.price)
            self.session.add(order_line)
            self.session.commit()

            messagebox.showinfo("Success", f"Order for {quantity} {box_name} box has been placed.")
            self.load_order_history()
        else:
            messagebox.showerror("Error", "Premade box not found.")

    def open_order_history(self):
        """Open a new window to display the order history."""
        order_history_window = tk.Toplevel(self.root)
        order_history_window.title("Order History")
        order_history_window.geometry("600x400")

        ttk.Label(order_history_window, text="Your Order History", font=("Arial", 16)).pack(pady=10)

        # Create a Treeview to display order history
        order_history_tree = ttk.Treeview(order_history_window, columns=("Order ID", "Item Name", "Quantity", "Price", "Total Cost"), show="headings")
        order_history_tree.heading("Order ID", text="Order ID")
        order_history_tree.heading("Item Name", text="Item Name")
        order_history_tree.heading("Quantity", text="Quantity")
        order_history_tree.heading("Price", text="Price")
        order_history_tree.heading("Total Cost", text="Total Cost")

        # Add vertical scrollbar
        scrollbar = ttk.Scrollbar(order_history_window, orient=tk.VERTICAL, command=order_history_tree.yview)
        order_history_tree.configure(yscroll=scrollbar.set)

        # Pack the Treeview and scrollbar
        order_history_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.load_order_history(order_history_tree)

    def update_order_status(self):
        """Update the status of a selected order."""
        order_id = self.staff_order_combobox.get()
        if not order_id:
            messagebox.showerror("Error", "Please select an order ID.")
            return

        # Update order status (this could be a dropdown to select status)
        order = self.session.query(Order).filter_by(order_id=order_id).first()
        if order:
            # Here you can set the new status (this could be from a dropdown in the GUI)
            order.status = "Processed"  # Update to the desired status
            self.session.commit()
            messagebox.showinfo("Success", f"Order {order_id} has been updated to 'Processed'.")
        else:
            messagebox.showerror("Error", "Order not found.")

    def load_order_history(self, order_history_tree):
        """Load the customer's order history into the treeview."""
        for row in order_history_tree.get_children():
            order_history_tree.delete(row)

        # Fetch orders for a specific customer (placeholder customer_id = 1)
        orders = self.session.query(Order).filter_by(customer_id=1).all()  # Placeholder customer_id
        for order in orders:
            order_lines = self.session.query(OrderLine).filter_by(order_id=order.order_id).all()
            total_cost = sum(line.quantity * line.price for line in order_lines)  # Calculate total cost

            for line in order_lines:
                order_history_tree.insert("", "end", values=(order.order_id, line.item_name, line.quantity, f"${line.price:.2f}", f"${total_cost:.2f}"))

# Initialize and run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
