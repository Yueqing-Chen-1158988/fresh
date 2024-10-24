import tkinter as tk
from tkinter import ttk, messagebox
from sqlalchemy import desc, func
from sqlalchemy.orm import sessionmaker
from database_setup import get_session
from models.customer import Customer, CorporateCustomer
from models.order import Order
from models.order_line import OrderLine
from models.payment import Payment
from models.staff import Staff
from models.vegetable_premadeBox import Vegetable, PremadeBox
from werkzeug.security import check_password_hash

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Vegetable Ordering System")
        self.root.geometry("800x800")

        self.session = get_session()  # Initialize database session

        # Initialize login screen
        self.show_login()

    def show_login(self):
        """Display the login screen."""
        self.login_frame = ttk.Frame(self.root)
        self.login_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(self.login_frame, text="Login", font=("Arial", 24)).pack(pady=20)

        ttk.Label(self.login_frame, text="Username:").pack(pady=5)
        self.username_entry = ttk.Entry(self.login_frame)
        self.username_entry.pack(pady=5)

        ttk.Label(self.login_frame, text="Password:").pack(pady=5)
        self.password_entry = ttk.Entry(self.login_frame, show="*")
        self.password_entry.pack(pady=5)

        self.login_button = ttk.Button(self.login_frame, text="Login", command=self.authenticate_user)
        self.login_button.pack(pady=20)

    def authenticate_user(self):
        """Authenticate the user based on the username and password."""
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password.")
            return

        # Check if user is a Customer
        customer = self.session.query(Customer).filter_by(username=username).first()
        
        if customer and check_password_hash(customer.password_hash, password):
            self.user_role = "customer"
            self.customer_id = customer.customer_id
            self.show_main_interface()
            return

        # Check if user is Staff
        staff = self.session.query(Staff).filter_by(username=username).first()
        
        if staff and check_password_hash(staff.password_hash, password):
            self.user_role = "staff"
            self.staff_id = staff.staff_id
            self.show_main_interface()
            return

        # Invalid credentials
        messagebox.showerror("Error", "Invalid username or password.")

    def show_main_interface(self):
        """Display the main interface based on the user role after successful login."""
        self.login_frame.pack_forget()  # Hide login frame

        # Create a main frame
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Create a notebook (tabbed interface)
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Create tabs
        self.customer_tab = ttk.Frame(self.notebook)
        self.staff_tab = ttk.Frame(self.notebook)

        if self.user_role == "customer":
            self.notebook.add(self.customer_tab, text="Customer")
            self.init_customer_functions()
        elif self.user_role == "staff":
            self.notebook.add(self.staff_tab, text="Staff")
            self.init_staff_functions()

    def init_customer_functions(self):
        """Initialize customer functionalities."""
        # Place Order Section
        ttk.Label(self.customer_tab, text="Place an Order", font=("Arial", 16)).pack(pady=10)

        self.order_frame = ttk.LabelFrame(self.customer_tab, text="Order Form")
        self.order_frame.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

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

        # Customer Selection
        ttk.Label(self.staff_tab, text="Enter Customer Email:").pack(padx=5, pady=5)
        self.customer_email_entry = ttk.Entry(self.staff_tab)
        self.customer_email_entry.pack(padx=5, pady=5)

        # Vegetable Selection
        ttk.Label(self.staff_tab, text="Select Vegetable:").pack(padx=5, pady=5)
        self.staff_vegetable_combobox = ttk.Combobox(self.staff_tab, values=self.get_vegetable_names())
        self.staff_vegetable_combobox.pack(padx=5, pady=5)

        # Quantity Entry
        ttk.Label(self.staff_tab, text="Quantity:").pack(padx=5, pady=5)
        self.staff_quantity_entry = ttk.Entry(self.staff_tab)
        self.staff_quantity_entry.pack(padx=5, pady=5)

        # Submit Order Button
        self.staff_submit_order_button = ttk.Button(self.staff_tab, text="Submit Order", command=self.submit_staff_order)
        self.staff_submit_order_button.pack(pady=10)

        # Update Order Status Section
        ttk.Label(self.staff_tab, text="Update Order Status", font=("Arial", 16)).pack(pady=10)
        ttk.Label(self.staff_tab, text="Enter Order ID:").pack(padx=5, pady=5)
        self.order_id_entry = ttk.Entry(self.staff_tab)
        self.order_id_entry.pack(padx=5, pady=5)

        ttk.Label(self.staff_tab, text="Select New Status:").pack(padx=5, pady=5)
        self.status_combobox = ttk.Combobox(self.staff_tab, values=["Pending", "Shipped", "Delivered", "Canceled"])
        self.status_combobox.pack(padx=5, pady=5)

        # Update Order Button
        self.update_status_button = ttk.Button(self.staff_tab, text="Update Status", command=self.update_order_status)
        self.update_status_button.pack(pady=10)

        # Customer Lookup Section
        ttk.Label(self.staff_tab, text="Customer Lookup", font=("Arial", 16)).pack(pady=10)
        ttk.Label(self.staff_tab, text="Enter Customer Email:").pack(padx=5, pady=5)
        self.customer_search_entry = ttk.Entry(self.staff_tab)
        self.customer_search_entry.pack(padx=5, pady=5)

        self.customer_details_label = ttk.Label(self.staff_tab, text="")
        self.customer_details_label.pack(padx=5, pady=5)

        # Search Button
        self.search_customer_button = ttk.Button(self.staff_tab, text="Search", command=self.view_customer_details)
        self.search_customer_button.pack(pady=10)

        # Report Section
        ttk.Label(self.staff_tab, text="Generate Reports", font=("Arial", 16)).pack(pady=10)
        self.report_combobox = ttk.Combobox(self.staff_tab, values=["Sales", "Customer List", "Item Popularity"])
        self.report_combobox.pack(padx=5, pady=5)

        self.generate_report_button = ttk.Button(self.staff_tab, text="Generate Report", command=self.generate_report)
        self.generate_report_button.pack(pady=10)

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
        new_order = Order(customer_id=customer.customer_id, order_type='vegetable', delivery_option='collect')
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
    
    def close(self):
        """Close the application and the session."""
        self.session.close()
        self.root.quit()

# Initialize and run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.protocol("WM_DELETE_WINDOW", app.close)
    root.mainloop()
