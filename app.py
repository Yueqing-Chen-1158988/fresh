import tkinter as tk
from database_setup import get_session
from models.order import Order
from views.login_view import LoginView
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Fresh Harvest Delivery")
        self.root.geometry("800x800")

        self.session = get_session()  # Initialize database session

        # Initialize login screen
        LoginView(self.root, self.session)
    
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
