### Project Structure

The following is an overview of the main files and directories in the project:

- **app.py**  
  Entry point to start the application.

- **models/**  
  Contains SQLAlchemy models such as `Customer`, `Order`, and `Payment`, which define the database structure.

- **controllers/**  
  Contains the business logic and manages the interactions between models and views.

- **views/**  
  Contains Tkinter views that form the graphical user interface (GUI).

- **database_setup.py**  
  Responsible for setting up and initializing database tables.

- **test/**  
  Contains unit tests to verify the functionality of different components in the application.

### Installation
#### Install Dependencies

```bash
pip install -r requirements.txt
```

#### Database Setup

```bash
python database_setup.py
```

#### Populate data to Database

```bash
python populate_data.py
```

### Running the Application
#### Start the Application

To launch the application, install dependencies:
```bash
python app.py
```

Run the following command in your terminal:


#### Login as Customer or Staff

- **Customer**: Can place orders, view order history, and make payments.
  - **Account Details**: 
    - Username: `ann`
    - Password: `password123`
  
- **Staff**: Can view customer details, manage orders, and generate reports.
  - **Account Details**:
    - Username: `ella`
    - Password: `password123`

### Running Tests

To run the unit tests for the application, use the following command:

```bash
pytest
```

