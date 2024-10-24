from tkinter import ttk

class StaffView:
    def __init__(self, root, session, staff_id, staff_tab):
        self.root = root
        self.session = session
        self.staff_id = staff_id
        self.staff_tab = staff_tab
        self.init_staff_interface()

    def init_staff_interface(self):
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

