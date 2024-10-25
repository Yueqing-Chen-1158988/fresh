from tkinter import messagebox
from models.order import Order
from models.order_line import OrderLine
from models.vegetable_premadeBox import PremadeBox, Vegetable

def get_vegetable_names(session):
    """Fetch vegetable names from the database."""
    vegetables = session.query(Vegetable).all()
    return [veg.name for veg in vegetables]

def get_premade_box_sizes(session):
    """Fetch premade box sizes from the database."""
    boxes = session.query(PremadeBox).all()
    return [box.size for box in boxes]

def update_vegetable_info(event, session, vegetable_combobox, price_label, unit_label):
    """Update the price and unit labels based on the selected vegetable."""
    vegetable_name = vegetable_combobox.get()
    vegetable = session.query(Vegetable).filter_by(name=vegetable_name).first()
    print("update_vegetable_info >>>")
    print(vegetable)
    
    if vegetable:
        price_label.config(text=f"${vegetable.price_per_unit:.2f}")
        unit_label.config(text=vegetable.unit)  # Assuming you have a unit attribute in your Vegetable model
    else:
        price_label.config(text="")
        unit_label.config(text="")


                
