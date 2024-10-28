from tkinter import ttk, messagebox
from controllers.staff_controller import StaffController

class StaffView:
    def __init__(self, root, session, staff_id, staff_tab):
        self.root = root
        self.session = session
        self.staff_id = staff_id
        self.staff_tab = staff_tab
        self.controller = StaffController(session)
        self.init_staff_interface()

    def init_staff_interface(self):
        """Initialize staff functionalities."""
        ttk.Label(self.staff_tab, text="Staff Dashboard", font=("Arial", 18, "bold")).pack(pady=10)

        # --- View All Vegetables and Premade Boxes ---
        ttk.Label(self.staff_tab, text="View Vegetables and Premade Boxes", font=("Arial", 16)).pack(pady=10)
        self.view_items_button = ttk.Button(self.staff_tab, text="View All Items", command=self.view_all_items)
        self.view_items_button.pack(pady=5)

        # --- View All Orders (Current and Previous) ---
        ttk.Label(self.staff_tab, text="View Orders", font=("Arial", 16)).pack(pady=10)
        self.order_type_combobox = ttk.Combobox(self.staff_tab, values=["Current Orders", "Previous Orders"])
        self.order_type_combobox.set("Select Order Type")
        self.order_type_combobox.pack(pady=5)
        self.view_orders_button = ttk.Button(self.staff_tab, text="View Orders", command=self.view_orders)
        self.view_orders_button.pack(pady=5)

        # --- Update Order Status ---
        ttk.Label(self.staff_tab, text="Update Order Status", font=("Arial", 16)).pack(pady=10)
        ttk.Label(self.staff_tab, text="Enter Order ID:").pack(pady=5)
        self.order_id_entry = ttk.Entry(self.staff_tab)
        self.order_id_entry.pack(pady=5)
        self.status_combobox = ttk.Combobox(self.staff_tab, values=["Pending", "Shipped", "Delivered", "Cancelled"])
        self.status_combobox.set("Select Status")
        self.status_combobox.pack(pady=5)
        self.update_status_button = ttk.Button(self.staff_tab, text="Update Status", command=self.update_order_status)
        self.update_status_button.pack(pady=10)

        # --- Customer Lookup ---
        ttk.Label(self.staff_tab, text="Customer Lookup", font=("Arial", 16)).pack(pady=10)
        ttk.Label(self.staff_tab, text="Enter Customer Email:").pack(pady=5)
        self.customer_search_entry = ttk.Entry(self.staff_tab)
        self.customer_search_entry.pack(pady=5)
        self.search_customer_button = ttk.Button(self.staff_tab, text="Search Customer", command=self.view_customer_details)
        self.search_customer_button.pack(pady=5)
        self.customer_details_label = ttk.Label(self.staff_tab, text="", font=("Arial", 10))
        self.customer_details_label.pack(pady=5)

        # --- Generate Customer List ---
        self.generate_customer_list_button = ttk.Button(self.staff_tab, text="Generate Customer List", command=self.generate_customer_list)
        self.generate_customer_list_button.pack(pady=10)

        # --- Generate Sales Reports ---
        ttk.Label(self.staff_tab, text="Generate Sales Report", font=("Arial", 16)).pack(pady=10)
        self.sales_report_combobox = ttk.Combobox(self.staff_tab, values=["Weekly Sales", "Monthly Sales", "Yearly Sales"])
        self.sales_report_combobox.set("Select Timeframe")
        self.sales_report_combobox.pack(pady=5)
        self.generate_sales_report_button = ttk.Button(self.staff_tab, text="Generate Sales Report", command=self.generate_sales_report)
        self.generate_sales_report_button.pack(pady=10)

        # --- View Most Popular Items ---
        self.view_popular_items_button = ttk.Button(self.staff_tab, text="View Most Popular Items", command=self.view_popular_items)
        self.view_popular_items_button.pack(pady=10)

    # --- Functions Calling StaffController ---

    def view_all_items(self):
        items_text = self.controller.get_all_items()
        messagebox.showinfo("All Items", items_text)

    def view_orders(self):
        order_type = self.order_type_combobox.get()
        orders_text = self.controller.get_orders_by_type(order_type)
        if orders_text:
            messagebox.showinfo(order_type, orders_text)
        else:
            messagebox.showerror("Error", "Please select a valid order type.")

    def update_order_status(self):
        order_id = self.order_id_entry.get()
        new_status = self.status_combobox.get()
        success = self.controller.update_order_status(order_id, new_status)
        if success:
            messagebox.showinfo("Success", "Order status updated.")
        else:
            messagebox.showerror("Error", "Order ID not found.")

    def view_customer_details(self):
        email = self.customer_search_entry.get()
        details = self.controller.get_customer_details(email)
        if details:
            self.customer_details_label.config(text=details)
        else:
            messagebox.showerror("Error", "Customer not found.")

    def generate_customer_list(self):
        customer_list = self.controller.get_customer_list()
        messagebox.showinfo("Customer List", customer_list)

    def generate_sales_report(self):
        timeframe = self.sales_report_combobox.get()
        report = self.controller.generate_sales_report(timeframe)
        if report:
            messagebox.showinfo(f"{timeframe} Report", report)
        else:
            messagebox.showerror("Error", "Please select a valid timeframe.")

    def view_popular_items(self):
        popular_items_text = self.controller.get_popular_items()
        messagebox.showinfo("Popular Items", popular_items_text)
