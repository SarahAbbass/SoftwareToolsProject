import sqlite3

def connect_to_db():
    conn = sqlite3.connect('database.db')
    return conn

################################### Customers #######################################
# creating customers table and functionalities
def create_customers_table():
    """Create the 'customers' table in the database if it does not exist.
    """
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
                 marital_status TEXT,
                 wallet_balance REAL DEFAULT 0.0
            );
        ''')
        conn.commit()
        print("Customer table created successfully!")
    except:
        print("Customer table creation failed -")
    finally:
        conn.close()

def insert_customer(customer): 
    """Insert a new customer into the database.

    :param customer: A dictionary representing the customer
    :type customer: dict
    :return: A dictionary representing the inserted customer
    :rtype: dict
    """
    inserted_customer = {} 
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO customers (full_name, username, password, address, age, gender, marital_status, wallet_balance) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (customer['full_name'], customer['username'], customer['password'], customer['address'], customer['age'], customer['gender'], customer['marital_status'], customer['wallet_balance'])) 
        conn.commit()
        inserted_customer = get_customer_by_username(cur.lastrowid)
    except sqlite3.IntegrityError as e:
        conn.rollback()
        return {'error': f'Error: {str(e)}. The username must be unique.'}
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
    "marital_status": "Single",
    "wallet_balance": 0.0
}

customer_Malak = {
    "full_name": "Malak Saleh",
    "username": "MalakS", 
    "password": "passwordMalak",
    "address": "Beirut, Lebanon",
    "age": 34,
    "gender": "Female",
    "marital_status": "Married",
    "wallet_balance": 3.0
}

def get_customers(): 
    """Retrieve a list of all customers.

    :return: List of dictionaries, each representing a customer
    :rtype: list
    """
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
            customer["wallet_balance"] = i["wallet_balance"]
            customers.append(customer)
    except:
        customers = []
    return customers

def get_customer_by_username(username): 
    """Retrieve customer information based on the provided username.

    :param username: The username of the customer
    :type username: str
    :return: A dictionary representing the customer if found, else None
    :rtype: dict or None
    """
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
        customer["wallet_balance"] = row["wallet_balance"]
    except:
        customer = {}
    return customer

def update_customer(customer): 
    """Update customer information in the database.

    :param customer: A dictionary representing the updated customer information
    :type customer: dict
    :return: A dictionary representing the updated customer
    :rtype: dict
    """
    updated_customer = {} 
    try:
        conn = connect_to_db() 
        cur = conn.cursor()
        cur.execute("UPDATE customers SET full_name = ?, password = ?, address = ?, age = ?, gender = ?, marital_status = ?, wallet_balance = ? WHERE username = ?",
                    (customer['full_name'], customer['password'], customer['address'], customer['age'], customer['gender'], customer['marital_status'], customer["wallet_balance"], customer["username"]))
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
    """Delete a customer based on the provided username.

    :param username: The username of the customer to be deleted
    :type username: str
    :return: A message representing either the success or the failure of deletion
    :rtype: str
    """
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

################################### Inventory #######################################
#creating inventory table and functionalities
def create_inventory_table():
    """Create the 'inventory' table in the database if it does not exist.
    """
    try:
        conn = connect_to_db()
        conn.execute('''
            CREATE TABLE IF NOT EXISTS inventory(
                 good_id INTEGER PRIMARY KEY,
                 name TEXT UNIQUE NOT NULL,
                 category TEXT NOT NULL,
                 price INTEGER NOT NULL,
                 description TEXT,
                 count INTEGER
            );
        ''')
        conn.commit()
        print("Inventory table created successfully!")
    except:
        print("Inventory table creation failed -")
    finally:
        conn.close()

def insert_good(good): 
    """Insert a new good into the database.

    :param good: A dictionary representing the good
    :type good: dict
    :return: A dictionary representing the inserted good
    :rtype: dict
    """
    inserted_good = {} 
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO inventory (name, category, price, description, count) VALUES (?, ?, ?, ?, ?)",
                    (good['name'], good['category'], good['price'], good['description'], good['count'])) 
        conn.commit()
        inserted_good = get_good_by_good_id(cur.lastrowid)
    except: 
        conn().rollback()
    finally: 
        conn.close()
    return inserted_good

ahmad_tea = {
    "name": "Ahmad Tea",
    "category": "Food", 
    "price": 1.3,
    "description": "Black Tea",
    "count": 22
}

dollys = {
    "name": "Dolly's Ketchup",
    "category": "Food", 
    "price": 0.8,
    "description": "Tomato Ketchup",
    "count": 15
}

def get_goods(): 
    """Retrieve a list of all goods.

    :return: List of dictionaries, each representing a good
    :rtype: list
    """
    goods = []
    try:
        conn = connect_to_db() 
        conn.row_factory = sqlite3.Row
        cur = conn.cursor() 
        cur.execute("SELECT * FROM inventory") 
        rows = cur.fetchall()
        
        # convert row objects to dictionary 
        for i in rows:
            good = {}
            good["good_id"] = i["good_id"] 
            good["name"] = i["name"] 
            good["category"] = i["category"] 
            good["price"] = i["price"] 
            good["description"] = i["description"] 
            good["count"] = i["count"]
            goods.append(good)
    except:
        goods = []
    return goods

def get_good_by_good_id(good_id): 
    """Retrieve good information based on the provided good_id.

    :param good_id: The good_id of the good
    :type good_id: str
    :return: A dictionary representing the good if found, else None
    :rtype: dict or None
    """
    good = {}
    try:
        conn = connect_to_db() 
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM inventory WHERE good_id = ?", (good_id,)) 
        row = cur.fetchone()
        
        # convert row object to dictionary 
        good["good_id"] = row["good_id"] 
        good["name"] = row["name"] 
        good["category"] = row["category"] 
        good["price"] = row["price"] 
        good["description"] = row["description"] 
        good["count"] = row["count"]
    except:
        good = {}
    return good

def update_good(good): 
    """Update good information in the database.

    :param good: A dictionary representing the updated good information
    :type good: dict
    :return: A dictionary representing the updated good
    :rtype: dict
    """
    updated_good = {} 
    try:
        conn = connect_to_db() 
        cur = conn.cursor()
        cur.execute("UPDATE inventory SET name = ?, category = ?, price = ?, description = ?, count = ? WHERE good_id = ?",
                    (good['name'], good['category'], good['price'], good['description'], good['count'], good["good_id"]))
        conn.commit()
        
        #return the user
        updated_good = get_good_by_good_id(good["good_id"])
    except: 
        conn.rollback()
        updated_good = {} 
    finally:
        conn.close() 
    return updated_good

def delete_good(good_id): 
    """Delete a good based on the provided good_id.

    :param good_id: The good_id of the good to be deleted
    :type good_id: str
    :return: A message representing either the success or the failure of deletion
    :rtype: str
    """
    message = {}
    try:
        conn = connect_to_db()
        conn.execute("DELETE from inventory WHERE good_id = ?", (good_id,))
        conn.commit()
        message["status"] = "Good deleted successfully."
    except: 
        conn.rollback()
        message["status"] = "Cannot delete good" 
    finally:
        conn.close()
    return message

def get_good_by_name(name):
    """Retrieve a good with the given name.

    :param name: The name of the good
    :type name: str
    :return: A good with the given name
    :rtype: dict or None
    """
    good = {}
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM inventory WHERE name = ?", (name,)) 
        row = cur.fetchone()
        
        # convert row object to dictionary 
        good["good_id"] = row["good_id"] 
        good["name"] = row["name"] 
        good["category"] = row["category"] 
        good["price"] = row["price"] 
        good["description"] = row["description"] 
        good["count"] = row["count"]
    except:
        good = {}
    return good

#create_customers_table()
#insert_customer(customer_Sara)
#insert_customer(customer_Malak)
#create_inventory_table()
#insert_good(ahmad_tea)
#insert_good(dollys)
