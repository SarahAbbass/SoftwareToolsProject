import sqlite3

def connect_to_db():
    conn = sqlite3.connect('database.db')
    return conn

def create_customers_table():
    try:
        conn = connect_to_db()
        conn.execute('''
            CREATE TABLE IF NOT EXISTS customers(
                 customer_id INTEGER PRIMARY KEY,
                 full_name TEXT NOT NULL,
                 username TEXT UNIQUE NOT NULL,
                 password TEXT NOT NULL,
                 address TEXT,
                 age INTEGER,
                 gender TEXT,
                 marital_status TEXT
            );
        ''')
        conn.commit()
        print("Customer table created successfully!")
    except:
        print("Customer table creation failed -")
    finally:
        conn.close()

def insert_customer(customer): 
    inserted_customer = {} 
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO customers (full_name, username, password, address, age, gender, marital_status) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (customer['full_name'], customer['username'], customer['password'], customer['address'], customer['age'], customer['gender'], customer['marital_status'])) 
        conn.commit()
        inserted_customer = get_customer_by_username(cur.lastrowid)
    except: 
        conn().rollback()
    finally: 
        conn.close()
    return inserted_customer

customer_Sara = {
    "full_name": "Sara Abbas",
    "username": "SaraA", 
    "password": "passwordSara",
    "address": "Geneva, Switzerland",
    "age": 22,
    "gender": "Female",
    "marital_status": "Single" 
}

customer_Malak = {
    "full_name": "Malak Saleh",
    "username": "MalakS", 
    "password": "passwordMalak",
    "address": "Beirut, Lebanon",
    "age": 34,
    "gender": "Female",
    "marital_status": "Married" 
}

def get_customer(): 
    customers = []
    try:
        conn = connect_to_db() 
        conn.row_factory = sqlite3.Row
        cur = conn.cursor() 
        cur.execute("SELECT * FROM customers") 
        rows = cur.fetchall()
        
        # convert row objects to dictionary 
        for i in rows:
            customer = {}
            customer["customer_id"] = i["customer_id"] 
            customer["full_name"] = i["full_name"] 
            customer["username"] = i["username"] 
            customer["password"] = i["password"] 
            customer["address"] = i["address"] 
            customer["age"] = i["age"]
            customer["gender"] = i["gender"]
            customer["marital_status"] = i["marital_status"] 
            customers.append(customer)
    except:
        customers = []
    return customers

def get_customer_by_username(username): 
    customer = {}
    try:
        conn = connect_to_db() 
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM customers WHERE username = ?", (username,)) 
        row = cur.fetchone()
        
        # convert row object to dictionary 
        customer["customer_id"] = row["customer_id"] 
        customer["full_name"] = row["full_name"] 
        customer["username"] = row["username"] 
        customer["password"] = row["password"] 
        customer["address"] = row["address"] 
        customer["age"] = row["age"]
        customer["gender"] = row["gender"]
        customer["marital_status"] = row["marital_status"] 
    except:
        customer = {}
    return customer

def update_customer(customer): 
    updated_customer = {} 
    try:
        conn = connect_to_db() 
        cur = conn.cursor()
        cur.execute("UPDATE customers SET full_name = ?, password = ?, address = ?, age = ?, gender = ?, marital_status = ? WHERE username = ?",
                    (customer['full_name'], customer['password'], customer['address'], customer['age'], customer['gender'], customer['marital_status'],))
        conn.commit()
        
        #return the user
        updated_customer = get_customer_by_username(customer["username"])
    except: 
        conn.rollback()
        updated_customer = {} 
    finally:
        conn.close() 
    return updated_customer

def delete_customer(username): 
    message = {}
    try:
        conn = connect_to_db()
        conn.execute("DELETE from customers WHERE username = ?", (username,))
        conn.commit()
        message["status"] = "Customer deleted successfully."
    except: 
        conn.rollback()
        message["status"] = "Cannot delete customer" 
    finally:
        conn.close()
    return message


#create_customers_table()
#insert_customer(customer_Sara)
#insert_customer(customer_Malak)
