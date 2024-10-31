from tkinter import Toplevel, messagebox, ttk
import tkinter as tk
from views.order_view import OrderView
from controllers.customer_controller import CustomerController

class CustomerView:
    def __init__(self, root, session, customer_id, customer_tab, logout):
        self.root = root
        self.session = session
        self.customer_id = customer_id
        self.customer_tab = customer_tab
        self.logout = logout
        self.controller = CustomerController(session)
        self.cart = []
        self.init_customer_interface()

    def init_customer_interface(self):
        """Initialize customer functionalities."""
        # Place Order Section
        ttk.Label(self.customer_tab, text="Place an Order", font=("Arial", 16)).pack(pady=10)
        self.order_frame = ttk.LabelFrame(self.customer_tab, text="Order Form")
        self.order_frame.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

        # Type Selection Dropdown
        ttk.Label(self.order_frame, text="Select Type:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.type_combobox = ttk.Combobox(self.order_frame, values=["Vegetable", "Premade Box"])
        self.type_combobox.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        self.type_combobox.bind("<<ComboboxSelected>>", self.update_type_selection)

        # Item Selection (updates based on type)
        ttk.Label(self.order_frame, text="Item:").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        self.item_combobox = ttk.Combobox(self.order_frame)
        self.item_combobox.grid(row=0, column=3, padx=5, pady=5, sticky=tk.W)
        self.item_combobox.bind("<<ComboboxSelected>>", self.update_item_details)

        # Price and Unit Labels
        ttk.Label(self.order_frame, text="Price per Unit:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.price_label = ttk.Label(self.order_frame, text="")
        self.price_label.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

        ttk.Label(self.order_frame, text="Unit:").grid(row=1, column=2, padx=5, pady=5, sticky=tk.W)
        self.unit_label = ttk.Label(self.order_frame, text="")
        self.unit_label.grid(row=1, column=3, padx=5, pady=5, sticky=tk.W)

        # Quantity Entry
        ttk.Label(self.order_frame, text="Quantity:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.quantity_entry = ttk.Entry(self.order_frame)
        self.quantity_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)

        # Add to Cart Button
        self.add_to_cart_button = ttk.Button(self.order_frame, text="Add to Cart", command=self.add_to_cart)
        self.add_to_cart_button.grid(row=2, column=2, columnspan=4, pady=10)

        # Delivery Option Section
        ttk.Label(self.order_frame, text="Delivery Option:").grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        self.delivery_option = "Collect"  # Default delivery option
        self.delivery_combobox = ttk.Combobox(self.order_frame, values=["Collect", "Delivery"])
        self.delivery_combobox.set("Collect") 
        self.delivery_combobox.grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)
        self.delivery_combobox.bind("<<ComboboxSelected>>", self.update_delivery_option_and_fee)

        # Delivery Fee
        ttk.Label(self.order_frame, text="Delivery Fee:").grid(row=4, column=2, padx=5, pady=5, sticky=tk.W)
        self.delivery_fee = 0.0  # Default delivery fee
        self.delivery_fee_label = ttk.Label(self.order_frame, text="$0.00")
        self.delivery_fee_label.grid(row=4, column=3, padx=5, pady=5, sticky=tk.W)

        # Cart Section
        self.cart_frame = ttk.LabelFrame(self.customer_tab, text="Cart")
        self.cart_frame.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
        self.cart_listbox = tk.Listbox(self.cart_frame, width=50, height=10)
        self.cart_listbox.pack(padx=5, pady=5)
        
        ttk.Label(self.cart_frame, text="Total Cost:").pack(padx=5, pady=5, anchor=tk.W)
        self.total_cost_label = ttk.Label(self.cart_frame, text="$0.00")
        self.total_cost_label.pack(padx=5, pady=5, anchor=tk.W)

        # Submit Order Button
        self.submit_order_button = ttk.Button(self.cart_frame, text="Submit Order", command=self.submit_order_handler)
        self.submit_order_button.pack(pady=10)

        # Payment Type Dropdown
        ttk.Label(self.cart_frame, text="Payment Type:").pack(pady=5, anchor=tk.W)
        self.payment_type_combobox = ttk.Combobox(self.cart_frame, values=["credit_card", "debit_card", "account"])
        self.payment_type_combobox.pack(anchor=tk.W)

        # Make Payment Button
        self.make_payment_button = ttk.Button(self.cart_frame, text="Make Payment", command=self.make_payment_handler)
        self.make_payment_button.pack(pady=5)

        # View Order History Button at the Bottom
        orderView = OrderView(self.root, self.session, self.customer_id)
        self.view_order_history_button = ttk.Button(self.customer_tab, text="View Order History", command=lambda: orderView.open_order_history(self.root, self.session, self.customer_id))
        self.view_order_history_button.pack(side=tk.LEFT, padx=10)

        # View Profile Button
        self.view_profile_button = ttk.Button(self.customer_tab, text="View Profile", command=self.view_profile)
        self.view_profile_button.pack(side=tk.LEFT, padx=10)

        # Logout Button
        self.logout_button = ttk.Button(self.customer_tab, text="Logout", command=self.logout)
        self.logout_button.pack(side=tk.LEFT, padx=10)

        # Ensure the UI refreshes
        self.customer_tab.update_idletasks()

    def update_type_selection(self, event):
        """Update item options based on selected type."""
        selected_type = self.type_combobox.get()
        self.item_combobox.set("")  
        self.price_label.config(text="")

        if selected_type == "Vegetable":
            self.item_combobox.config(values=self.controller.get_vegetable_names(self.session))
            self.unit_label.config(text="") 
        elif selected_type == "Premade Box":
            self.item_combobox.config(values=self.controller.get_premade_box_sizes(self.session))
            self.unit_label.config(text="N/A")

    def update_item_details(self, event):
        """Update price and unit labels based on selected item."""
        selected_type = self.type_combobox.get()
        selected_item = self.item_combobox.get()
        if selected_type == "Vegetable":
            self.controller.update_vegetable_info(event, self.session, self.item_combobox, self.price_label, self.unit_label)
        elif selected_type == "Premade Box":
            # For premade box, fetch and display only price
            price = self.get_premade_box_price(selected_item)
            self.price_label.config(text=f"${price:.2f}")
            self.unit_label.config(text="")

            self.show_box_contents_popup(selected_item)

    def show_box_contents_popup(self, box_size):
        """Show a pop-up displaying the contents of a selected box."""
        # Fetch the contents from the controller
        contents = self.controller.get_box_contents(self.session, box_size)
        
        # Create a new pop-up window
        popup = Toplevel()
        popup.title(f"Contents of {box_size}")
        popup.geometry("300x300")

        ttk.Label(popup, text=f"{box_size} Contents", font=("Arial", 14, "bold")).pack(pady=5)

        # Display each item in the box
        for content in contents:
            item_text = f"{content.vegetable.name} - {content.quantity} {content.vegetable.unit}"
            ttk.Label(popup, text=item_text).pack()

        tk.Button(popup, text="Close", command=popup.destroy).pack(pady=10)
        
    def add_to_cart(self):
        """Handler to add selected item to the cart and update cart details."""
        item_type = self.type_combobox.get()
        item_name = self.item_combobox.get()
        quantity = self.quantity_entry.get()
        price_per_unit = self.price_label.cget("text").strip("$")

        # Call controller to add item to cart
        cart_item = self.controller.add_item_to_cart(self.cart, item_type, item_name, quantity, price_per_unit)
        if cart_item:
            self.cart_listbox.insert(
                tk.END, 
                f"{cart_item['name']} - {cart_item['quantity']} x ${cart_item['price']:.2f} = ${cart_item['subtotal']:.2f}"
            )
            self.update_total_cost()

    def update_total_cost(self):
        """Calculate and display the total cost of items in the cart."""
        total = sum(item["subtotal"] for item in self.cart) + self.delivery_fee
        self.total_cost_label.config(text=f"${total:.2f}")

    def submit_order_handler(self):
        """Submit the order with items in the cart."""
        delivery_option = self.delivery_combobox.get()
        delivery_fee = self.delivery_fee
        self.order_id = self.controller.submit_order(self.session, self.customer_id, self.cart, delivery_option, delivery_fee)
        self.cart_listbox.delete(0, tk.END)
        self.cart.clear()
        self.update_total_cost()

    def update_delivery_option_and_fee(self, event):
        """Update the delivery fee based on the selected option."""
        self.delivery_option = self.delivery_combobox.get()
        if self.delivery_option == "Delivery":
            self.delivery_fee_label.config(text="$10.00") 
            self.delivery_fee = 10.0
        else:
            self.delivery_fee_label.config(text="$0.00")
            self.delivery_fee = 0.00
        self.update_total_cost()

    def get_premade_box_price(self, box_name):
        """Placeholder function to get premade box price."""
        box_prices = {"Small Box": 10.0, "Medium Box": 15.0, "Large Box": 20.0}
        return box_prices.get(box_name, 0.0)

    def view_profile(self):
        """Display customer profile information in a pop-up window."""
        profile = self.controller.get_customer_profile(self.session, self.customer_id)
        if profile:
            profile_info = f"Name: {profile.name}\nEmail: {profile.email}\nBalance: ${profile.balance:.2f}"
            
            # Check if it's a corporate customer and add additional details
            if hasattr(profile, 'credit_limit'):
                profile_info += f"\nCredit Limit: ${profile.credit_limit:.2f}\nDiscount Rate: {profile.discount_rate * 100:.0f}%"

            messagebox.showinfo("Customer Profile", profile_info)
        else:
            messagebox.showerror("Error", "Unable to load profile information.")

    def make_payment_handler(self):
        """Handler to initiate payment for the order."""
        payment_type = self.payment_type_combobox.get()
        if not payment_type:
            messagebox.showerror("Error", "Please select a payment type.")
            return

        if not hasattr(self, 'order_id') or self.order_id is None:
            messagebox.showerror("Error", "Please submit an order before making a payment.")
            return
        
        total_cost = float(self.total_cost_label.cget("text").strip("$"))
        self.controller.make_payment(self.session, self.order_id, payment_type, total_cost)
