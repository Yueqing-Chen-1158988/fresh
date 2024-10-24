from tkinter import ttk, messagebox
import tkinter as tk
from controllers.auth_controller import authenticate_user
from views.customer_view import CustomerView
from views.staff_view import StaffView

class LoginView:
    def __init__(self, root, session):
        self.root = root
        self.session = session
        self.login_frame = ttk.Frame(self.root)
        self.login_frame.pack(fill=tk.BOTH, expand=True)

        # UI elements
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
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password.")
            return

        # Call authentication logic
        success, role, user_id = authenticate_user(self.session, username, password)

        if success:
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

            if role == "customer":
                self.notebook.add(self.customer_tab, text="Customer")
                CustomerView(self.root, self.session, user_id, self.customer_tab)

            elif role == "staff":
                self.notebook.add(self.staff_tab, text="Staff")
                StaffView(self.root, self.session, user_id, self.staff_tab)
        else:
            messagebox.showerror("Error", "Invalid username or password.")
