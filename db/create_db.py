from database_setup import create_tables, drop_tables

def initialize_database():
     # Drop existing tables first
    drop_tables()
    
    create_tables()
    print("Database tables created successfully.")

if __name__ == '__main__':
    initialize_database()
