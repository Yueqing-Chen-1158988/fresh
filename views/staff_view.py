from tkinter import Toplevel, ttk, messagebox
from controllers.staff_controller import StaffController
import tkinter as tk

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
        ttk.Label(self.staff_tab, text="Staff Dashboard", font=("Arial", 18, "bold")).pack(pady=(10, 20))

        # Frame for Viewing Items
        item_frame = ttk.LabelFrame(self.staff_tab, text="Items", padding=(10, 10))
        item_frame.pack(pady=10, fill="x")

        self.view_vegetables_button = ttk.Button(item_frame, text="View All Vegetables", command=self.open_vegetable_window)
        self.view_vegetables_button.pack(side=tk.LEFT, padx=10)

        self.view_boxes_button = ttk.Button(item_frame, text="View All Premade Boxes", command=self.open_box_window)
        self.view_boxes_button.pack(side=tk.LEFT, padx=10)

        # Frame for Viewing Orders
        order_frame = ttk.LabelFrame(self.staff_tab, text="Orders", padding=(10, 10))
        order_frame.pack(pady=10, fill="x")

        self.order_type_combobox = ttk.Combobox(order_frame, values=["Current Orders", "Previous Orders"], state="readonly")
        self.order_type_combobox.set("Select Order Type")
        self.order_type_combobox.pack(side=tk.LEFT, padx=10)

        self.view_orders_button = ttk.Button(order_frame, text="View All Orders", command=self.open_orders_window)
        self.view_orders_button.pack(side=tk.LEFT, padx=10)

        # Frame for Viewing Customers
        customer_frame = ttk.LabelFrame(self.staff_tab, text="Customers", padding=(10, 10))
        customer_frame.pack(pady=10, fill="x")

        # Button to View All Customers
        self.view_all_customers_button = ttk.Button(customer_frame, text="View Customers and Details", command=self.view_all_customers)
        self.view_all_customers_button.pack(side=tk.LEFT, padx=10)

        # Frame for Generating Reports
        report_frame = ttk.LabelFrame(self.staff_tab, text="Generate Sales Report", padding=(10, 10))
        report_frame.pack(pady=10, fill="x")

        # Dropdown for selecting the timeframe
        ttk.Label(report_frame, text="Select Timeframe:").grid(row=0, column=0, padx=5, pady=5)
        self.timeframe_combo = ttk.Combobox(report_frame, values=["Week", "Month", "Year"], state="readonly")
        self.timeframe_combo.grid(row=0, column=1, padx=5, pady=5)
        
        # Button to generate the report
        self.generate_report_button = ttk.Button(report_frame, text="Generate Report", command=self.generate_sales_report)
        self.generate_report_button.grid(row=0, column=2, padx=5, pady=5)
    
        # Frame for Viewing Popular Items
        popular_items_frame = ttk.LabelFrame(self.staff_tab, text="Most Popular Items", padding=(10, 10))
        popular_items_frame.pack(pady=10, fill="x")

        self.view_popular_items_button = ttk.Button(popular_items_frame, text="View Most Popular Items", command=self.show_popular_items)
        self.view_popular_items_button.pack(side=tk.LEFT, padx=10)

        # Logout Button
        self.logout_button = ttk.Button(self.staff_tab, text="Logout", command=self.logout)
        self.logout_button.pack(pady=20)

    def open_vegetable_window(self):
        """Open a new window to view all vegetables."""
        vegetable_window = Toplevel(self.root)
        vegetable_window.title("View All Vegetables")

        # Create a Treeview to display vegetables
        veg_tree = ttk.Treeview(vegetable_window, columns=("ID", "Name", "Unit", "Price"), show="headings")
        veg_tree.heading("ID", text="ID")
        veg_tree.heading("Name", text="Name")
        veg_tree.heading("Unit", text="Unit")
        veg_tree.heading("Price", text="Price")
        veg_tree.pack(side="left", fill="both", expand=True)

        # Add a vertical scrollbar for the Treeview
        veg_scroll = ttk.Scrollbar(vegetable_window, orient="vertical", command=veg_tree.yview)
        veg_tree.configure(yscrollcommand=veg_scroll.set)
        veg_scroll.pack(side="right", fill="y")

        # Fetch and display vegetables
        self.view_all_vegetables(veg_tree)

    def open_box_window(self):
        """Open a new window to view all premade boxes."""
        box_window = Toplevel(self.root)
        box_window.title("View All Premade Boxes")

        # Create a Treeview to display premade boxes
        box_tree = ttk.Treeview(box_window, columns=("ID", "Size", "Price"), show="headings")
        box_tree.heading("ID", text="ID")
        box_tree.heading("Size", text="Size")
        box_tree.heading("Price", text="Price")
        box_tree.pack(side="left", fill="both", expand=True)

        # Add a vertical scrollbar for the Treeview
        box_scroll = ttk.Scrollbar(box_window, orient="vertical", command=box_tree.yview)
        box_tree.configure(yscrollcommand=box_scroll.set)
        box_scroll.pack(side="right", fill="y")

        # Fetch and display premade boxes
        self.view_all_boxes(box_tree)

    def open_orders_window(self):
        """Open a new window to view all orders."""
        orders_window = Toplevel(self.root)
        orders_window.title("View All Orders")
        orders_window.geometry("600x400")

        ttk.Label(orders_window, text="Order History", font=("Arial", 16)).pack(pady=10)

        # Frame to hold both the table and buttons
        content_frame = ttk.Frame(orders_window)
        content_frame.pack(fill=tk.BOTH, expand=True)

        # Create a Treeview to display orders
        order_tree = ttk.Treeview(content_frame, columns=("Order ID", "Customer", "Status"), show="headings")
        order_tree.heading("Order ID", text="Order ID")
        order_tree.heading("Customer", text="Customer")
        order_tree.heading("Status", text="Status")
        order_tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Add a vertical scrollbar for the Treeview
        order_scroll = ttk.Scrollbar(content_frame, orient="vertical", command=order_tree.yview)
        order_tree.configure(yscrollcommand=order_scroll.set)
        order_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # Fetch and display orders
        self.view_orders(order_tree)

        # Buttons for order details, update status, and cancel order
        button_frame = ttk.Frame(content_frame)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

        # Buttons for viewing order details, updating status, and canceling order
        self.view_order_details_button = ttk.Button(button_frame, text="View Order Details", command=lambda: self.on_order_details(order_tree))
        self.view_order_details_button.pack(side=tk.LEFT, padx=10)

        self.update_order_status_button = ttk.Button(button_frame, text="Update Status", command=lambda: self.open_update_status_window(order_tree))
        self.update_order_status_button.pack(side=tk.LEFT, padx=10)

        self.cancel_order_button = ttk.Button(button_frame, text="Cancel Order", command=lambda: self.cancel_order(order_tree))
        self.cancel_order_button.pack(side=tk.LEFT, padx=10)

    def view_all_vegetables(self, treeview):
        """Fetch and display all vegetables in the Treeview."""
        vegetables = self.controller.get_all_vegetables()
        for item in treeview.get_children():
            treeview.delete(item)
        for veg in vegetables:
            treeview.insert("", "end", values=(veg.vegetable_id, veg.name, veg.unit, veg.price_per_unit))

    def view_all_boxes(self, treeview):
        """Fetch and display all premade boxes in the Treeview."""
        boxes = self.controller.get_all_premade_boxes()
        for item in treeview.get_children():
            treeview.delete(item)
        for box in boxes:
            treeview.insert("", "end", values=(box.box_id, box.size, box.price))

    def view_orders(self, treeview):
        """Fetch and display current/previous orders in the Treeview."""
        order_type = self.order_type_combobox.get()
        orders = self.controller.get_orders_by_type(order_type)
        
        # Clear the treeview
        for item in treeview.get_children():
            treeview.delete(item)

        # Check if any orders were returned
        if not orders:
            messagebox.showinfo("Info", "No orders found for the selected type.")
            return

        # Insert each order into the treeview
        for order in orders:
            customer_name = order.customer.name if order.customer else "Unknown" 
            treeview.insert("", "end", values=(order.order_id, customer_name, order.status))

    def on_order_details(self, order_tree):
        """Handle the order details button click."""
        selected_item = order_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select an order to view details.")
            return

        order_id = order_tree.item(selected_item)['values'][0]
        # Add logic here to display order details
        self.view_order_detail(order_id)

    def view_order_detail(self, order_id):
        """Display detailed information for a specific order, including order lines."""
        order_detail = self.controller.get_order_detail(order_id)
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
        veg_tree.column("Item", width=80)
        veg_tree.heading("Quantity", text="Quantity")
        veg_tree.column("Quantity", width=40)
        veg_tree.heading("Unit", text="Unit")
        veg_tree.column("Unit", width=40)
        veg_tree.heading("Price", text="Price")
        veg_tree.column("Price", width=40)
        veg_tree.pack(fill=tk.BOTH, expand=True)

        # Premade Box Items Treeview
        box_tree = ttk.Treeview(box_frame, columns=("Size", "Quantity", "Price"), show="headings")
        box_tree.heading("Size", text="Size")
        box_tree.column("Size", width=80)
        box_tree.heading("Quantity", text="Quantity")
        box_tree.column("Quantity", width=40)
        box_tree.heading("Price", text="Price")
        box_tree.column("Price", width=40)
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

    def open_update_status_window(self, order_tree):
        """Open a new window to update the status of a selected order."""
        selected_item = order_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select an order to update.")
            return

        # Get the selected order's ID and current status
        order_id = order_tree.item(selected_item)["values"][0]
        current_status = order_tree.item(selected_item)["values"][2]

        # Create the update status window
        update_window = Toplevel(self.root)
        update_window.title("Update Order Status")
        update_window.geometry("300x200")

        ttk.Label(update_window, text=f"Order ID: {order_id}", font=("Arial", 12)).pack(pady=10)
        ttk.Label(update_window, text=f"Current Status: {current_status}", font=("Arial", 12)).pack(pady=5)

        # Status combobox for selecting new status
        ttk.Label(update_window, text="New Status:").pack(pady=5)
        status_combobox = ttk.Combobox(update_window, values=["Processing", "Completed", "Cancelled"], state="readonly")
        status_combobox.set("Select Status")
        status_combobox.pack(pady=5)

        # Button to confirm status update
        confirm_button = ttk.Button(update_window, text="Update Status", command=lambda: self.confirm_status_update(order_id, status_combobox, update_window, order_tree))
        confirm_button.pack(pady=10)

    def confirm_status_update(self, order_id, status_combobox, update_window, order_tree):
        """Confirm and update the order status."""
        new_status = status_combobox.get()

        if new_status == "Select Status" or not new_status:
            messagebox.showwarning("Warning", "Please select a new status.")
            return

        # Call the controller to update the status
        success = self.controller.update_order_status(order_id, new_status)
        if success:
            messagebox.showinfo("Success", "Order status updated.")
            update_window.destroy()  # Close the update status window

            # Refresh the displayed orders in the main order window
            self.view_orders(order_tree)
        else:
            messagebox.showerror("Error", "Order ID not found.")

    def cancel_order(self, order_tree):
        """Cancel an order that is not completed."""
        selected_item = order_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select an order to cancel.")
            return
        
        order_id = order_tree.item(selected_item)["values"][0]
        success = self.controller.cancel_order(order_id)
        if success:
            messagebox.showinfo("Success", "Order canceled successfully.")
            self.view_all_orders(order_tree)  # Refresh the order list
        else:
            messagebox.showerror("Error", "Order ID not found or cannot be canceled.")

    def view_all_customers(self):
        """Open a new window to display all customers with a search box."""
        customer_window = Toplevel(self.root)
        customer_window.title("Customer List")
        customer_window.geometry("600x400")

        # Search by Name Frame
        search_frame = ttk.Frame(customer_window)
        search_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(search_frame, text="Search by Name:").pack(side="left")
        self.customer_search_name_entry = ttk.Entry(search_frame)
        self.customer_search_name_entry.pack(side="left", padx=5)
        search_button = ttk.Button(search_frame, text="Search", command=lambda: self.filter_customers(customer_tree))
        search_button.pack(side="left", padx=5)

        # Treeview for Displaying Customer List
        columns = ("Customer ID", "Name", "Username", "Email", "Balance", "Credit Limit")
        customer_tree = ttk.Treeview(customer_window, columns=columns, show="headings")
        customer_tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Define column headings
        for col in columns:
            customer_tree.heading(col, text=col)
            customer_tree.column(col, anchor="w", width=100)

        # Insert customer data
        customers = self.controller.get_all_customers()
        for customer in customers:
            # Display the credit limit if it exists, otherwise "N/A"
            credit_limit = getattr(customer, 'credit_limit', "N/A")
            customer_tree.insert("", "end", values=(
                customer.customer_id, customer.name, customer.username,
                customer.email, customer.balance, credit_limit
            ))

        # Store Treeview for filtering
        self.customer_tree = customer_tree

        # Add a close button
        close_button = ttk.Button(customer_window, text="Close", command=customer_window.destroy)
        close_button.pack(pady=10)

    def filter_customers(self, customer_tree):
        """Filter customers by name based on search input."""
        search_name = self.customer_search_name_entry.get().strip().lower()
        for item in customer_tree.get_children():
            customer_tree.delete(item)

        # Re-populate Treeview with filtered customers
        filtered_customers = self.controller.get_customers_by_name(search_name)
        for customer in filtered_customers:
            credit_limit = customer.credit_limit if hasattr(customer, 'credit_limit') else "N/A"
            customer_tree.insert("", "end", values=(customer.customer_id, customer.name, customer.username, customer.email, customer.balance, credit_limit))

    def generate_sales_report(self):
        """Handler for the 'Generate Report' button."""
        timeframe = self.timeframe_combo.get()
        if not timeframe:
            messagebox.showwarning("Warning", "Please select a timeframe.")
            return
        
        # Call the controller to get sales data
        sales_data = self.controller.generate_sales_report(timeframe)
        if sales_data:
            self.show_sales_report_popup(sales_data)
        else:
            messagebox.showinfo("Info", "No sales data available for the selected timeframe.")

    def show_sales_report_popup(self, sales_data):
        """Display the sales report in a popup data table."""
        report_window = Toplevel(self.root)
        report_window.title("Sales Report")
        report_window.geometry("500x300")
        
        # Treeview for displaying sales data
        report_tree = ttk.Treeview(report_window, columns=("Date", "Total Sales"), show="headings")
        report_tree.heading("Date", text="Date")
        report_tree.heading("Total Sales", text="Total Sales")
        report_tree.column("Date", anchor="w", width=150)
        report_tree.column("Total Sales", anchor="w", width=150)
        report_tree.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Insert sales data
        for row in sales_data:
            report_tree.insert("", "end", values=row)

        # Add a close button
        close_button = ttk.Button(report_window, text="Close", command=report_window.destroy)
        close_button.pack(pady=10)

    def show_popular_items(self):
        """Display the most popular items in a new window."""
        # Retrieve the popular items data
        popular_items_data = self.controller.get_popular_items()

        # Create a new pop-up window
        popular_window = tk.Toplevel(self.root)
        popular_window.title("Most Popular Items")
        popular_window.geometry("300x300")
        popular_window.grab_set()

        # Create a Treeview to display popular items
        columns = ("Item Name", "Order Count")
        popular_items_tree = ttk.Treeview(popular_window, columns=columns, show="headings")
        popular_items_tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Define the headings
        popular_items_tree.heading("Item Name", text="Item Name", anchor="w")
        popular_items_tree.column("Item Name", width=80)
        popular_items_tree.heading("Order Count", text="Order Count", anchor="w")
        popular_items_tree.column("Order Count", width=40)

        # Insert popular items data into the Treeview
        for item, count in popular_items_data:
            popular_items_tree.insert("", "end", values=(item, count))

        # Add a close button
        close_button = ttk.Button(popular_window, text="Close", command=popular_window.destroy)
        close_button.pack(pady=10)

    def logout(self):
        """Logout the user and return to the login screen."""
        # Destroy the main frame
        if hasattr(self.root, 'main_frame'):
            self.root.main_frame.destroy()

        # Show the login view and reset fields
        if hasattr(self.root, 'login_view'):
            self.root.login_view.reset_fields()  # Clear username and password fields
            self.root.login_view.login_frame.pack(fill=tk.BOTH, expand=True)
        else:
            from views.login_view import LoginView
            self.root.login_view = LoginView(self.root, self.session)
            self.root.login_view.login_frame.pack(fill=tk.BOTH, expand=True)
