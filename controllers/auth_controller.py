from models.customer import Customer
from models.staff import Staff
from werkzeug.security import check_password_hash

def authenticate_user(session, username, password):
    # Check if user is Customer
    customer = session.query(Customer).filter_by(username=username).first()
    if customer and check_password_hash(customer.password_hash, password):
        return True, "customer", customer.customer_id

    # Check if user is Staff
    staff = session.query(Staff).filter_by(username=username).first()
    if staff and check_password_hash(staff.password_hash, password):
        return True, "staff", staff.staff_id

    # Invalid credentials
    return False, None, None
