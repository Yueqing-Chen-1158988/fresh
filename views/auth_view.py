from tkinter import ttk, messagebox
import tkinter as tk
from controllers.auth_controller import authenticate_user
from views.customer_view import CustomerView
from views.staff_view import StaffView

class AuthView:
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
        """Authenticate the user based on the entered username and password."""
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password.")
            return

        # Call authentication logic
        success, role, user_id = authenticate_user(self.session, username, password)

        if success:
            # Remove any existing main frames
            if hasattr(self.root, 'main_frame'):
                self.root.main_frame.destroy()

            self.login_frame.pack_forget()

            self.main_frame = ttk.Frame(self.root)
            self.main_frame.pack(fill=tk.BOTH, expand=True)
            self.root.main_frame = self.main_frame

            # Create a notebook to display different tabs
            self.notebook = ttk.Notebook(self.main_frame)
            self.notebook.pack(fill=tk.BOTH, expand=True)

            # Create tabs for customer and staff views
            self.customer_tab = ttk.Frame(self.notebook)
            self.staff_tab = ttk.Frame(self.notebook)

            # Display the appropriate tab based on the user role
            if role == "customer":
                self.notebook.add(self.customer_tab, text="Customer")
                CustomerView(self.root, self.session, user_id, self.customer_tab, self.logout)

            elif role == "staff":
                self.notebook.add(self.staff_tab, text="Staff")
                StaffView(self.root, self.session, user_id, self.staff_tab, self.logout)
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    def reset_fields(self):
        """Clear the username and password fields."""
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)

    def logout(self):
        """Logout the user and return to the login screen."""
        # Destroy the main frame and show the login frame
        if hasattr(self.root, 'main_frame'):
            self.root.main_frame.destroy()

        if hasattr(self.root, 'login_view'):
            self.root.login_view.reset_fields()  # Clear username and password fields
            self.root.login_view.login_frame.pack(fill=tk.BOTH, expand=True)
        else:
            self.root.login_view = AuthView(self.root, self.session)
            self.root.login_view.login_frame.pack(fill=tk.BOTH, expand=True)

        self.root.update_idletasks()