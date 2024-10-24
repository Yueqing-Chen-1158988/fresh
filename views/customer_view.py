from tkinter import ttk
import tkinter as tk

from controllers.customer_controller import get_premade_box_sizes, get_vegetable_names, open_order_history, submit_order, submit_premade_box_order, update_vegetable_info

class CustomerView:
    def __init__(self, root, session, customer_id, customer_tab):
        self.root = root
        self.session = session
        self.customer_id = customer_id
        self.customer_tab = customer_tab
        self.init_customer_interface()

    def init_customer_interface(self):
        """Initialize customer functionalities."""
        # Place Order Section
        ttk.Label(self.customer_tab, text="Place an Order", font=("Arial", 16)).pack(pady=10)

        self.order_frame = ttk.LabelFrame(self.customer_tab, text="Order Form")
        self.order_frame.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

        # Labels for price and unit
        ttk.Label(self.order_frame, text="Price per Unit:").grid(row=1, column=0, padx=5, pady=5)
        self.price_label = ttk.Label(self.order_frame, text="")
        self.price_label.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.order_frame, text="Unit:").grid(row=2, column=0, padx=5, pady=5)
        self.unit_label = ttk.Label(self.order_frame, text="")
        self.unit_label.grid(row=2, column=1, padx=5, pady=5)

        # Vegetable Selection Section
        ttk.Label(self.order_frame, text="Select Vegetable:").grid(row=0, column=0, padx=5, pady=5)
        self.vegetable_combobox = ttk.Combobox(self.order_frame, values=get_vegetable_names(self.session))
        self.vegetable_combobox.grid(row=0, column=1, padx=5, pady=5)
        self.vegetable_combobox.bind("<<ComboboxSelected>>", lambda event: update_vegetable_info(event, self.session, self.vegetable_combobox, self.price_label, self.unit_label))

        # Quantity Entry
        ttk.Label(self.order_frame, text="Quantity:").grid(row=3, column=0, padx=5, pady=5)
        self.quantity_entry = ttk.Entry(self.order_frame)
        self.quantity_entry.grid(row=3, column=1, padx=5, pady=5)

        # Submit Order Button
        self.submit_order_button = ttk.Button(self.order_frame, text="Submit Order", command=lambda:submit_order(self.session, self.root, self.vegetable_combobox, self.quantity_entry))
        self.submit_order_button.grid(row=4, columnspan=2, pady=10)


        # View Order History Button
        self.view_order_history_button = ttk.Button(self.order_frame, text="View Order History", command=lambda:open_order_history(self.session, self.root))
        self.view_order_history_button.grid(row=5, columnspan=2, pady=10)


        # Premade Box Order Section
        ttk.Label(self.customer_tab, text="Order Premade Box", font=("Arial", 16)).pack(pady=10)

        self.box_frame = ttk.LabelFrame(self.customer_tab, text="Premade Box Order Form")
        self.box_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Premade Box Selection
        ttk.Label(self.box_frame, text="Select Premade Box:").grid(row=0, column=0, padx=5, pady=5)
        self.premade_box_combobox = ttk.Combobox(self.box_frame, values=get_premade_box_sizes(self.session))
        self.premade_box_combobox.grid(row=0, column=1, padx=5, pady=5)

        # Box Quantity Entry
        ttk.Label(self.box_frame, text="Quantity:").grid(row=1, column=0, padx=5, pady=5)
        self.box_quantity_entry = ttk.Entry(self.box_frame)
        self.box_quantity_entry.grid(row=1, column=1, padx=5, pady=5)

        # Submit Box Order Button
        self.submit_box_order_button = ttk.Button(self.box_frame, text="Submit Box Order", command=lambda:submit_premade_box_order(self.session, self.premade_box_combobox, self.box_quantity_entry))
        self.submit_box_order_button.grid(row=2, columnspan=2, pady=10)
        
