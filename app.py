import tkinter as tk
from db.database_setup import get_session
from models.order import Order
from views.login_view import LoginView
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Vegetable Ordering System")
        self.root.geometry("800x800")

        self.session = get_session()  # Initialize database session

        # Initialize login screen
        LoginView(self.root, self.session)


    def get_order_ids(self):
        """Fetch order IDs from the database for staff processing."""
        orders = self.session.query(Order).all()
        return [order.order_id for order in orders]

    
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
