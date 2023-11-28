import psycopg2
from datetime import datetime, date

def connect_to_db():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="435L",
            user="postgres",    
            password="ab"
        )
        return conn
    except psycopg2.Error as e:
        print(f"Unable to connect to the database. Error: {e}")

def create_customers_table():
    """Create the 'customers' table in the database if it does not exist.
    """
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS customers(
                 customer_id SERIAL PRIMARY KEY,
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
    except psycopg2.Error as e:
        print(f"Error creating 'customers' table: {e}")
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
        cur.execute("INSERT INTO customers (full_name, username, password, address, age, gender, marital_status, wallet_balance) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);",
            (customer['full_name'], customer['username'], customer['password'], customer['address'], customer['age'], customer['gender'], customer['marital_status'], customer['wallet_balance']))
        conn.commit()

        inserted_customer = get_customer_by_username(customer['username'])

    except psycopg2.Error as e:
        conn.rollback()
        return {'error': f'Error: {str(e)}. The username must be unique.'}
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
        cur = conn.cursor() 
        cur.execute("SELECT * FROM customers;") 
        rows = cur.fetchall()
        # convert row objects to dictionary 
        for i in rows:
            customer = {}
            customer["customer_id"] = i[0] 
            customer["full_name"] = i[1] 
            customer["username"] = i[2] 
            customer["password"] = i[3] 
            customer["address"] = i[4] 
            customer["age"] = i[5]
            customer["gender"] = i[6]
            customer["marital_status"] = i[7] 
            customer["wallet_balance"] = i[8]
            customers.append(customer)
    except psycopg2.Error as e:
        print(f"Error fetching customers: {e}")
    finally:
        conn.close() 
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
        cur = conn.cursor()
        cur.execute("SELECT * FROM customers WHERE username = %s", (username,))
        row = cur.fetchone()
        
        if row:
            customer["customer_id"] = row[0] 
            customer["full_name"] = row[1] 
            customer["username"] = row[2] 
            customer["password"] = row[3] 
            customer["address"] = row[4] 
            customer["age"] = row[5]
            customer["gender"] = row[6]
            customer["marital_status"] = row[7] 
            customer["wallet_balance"] = row[8]
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
        cur.execute(
            "UPDATE customers SET full_name = %s, password = %s, address = %s, age = %s, gender = %s, marital_status = %s, wallet_balance = %s WHERE username = %s;",
            (customer['full_name'], customer['password'], customer['address'], customer['age'], customer['gender'], customer['marital_status'], customer["wallet_balance"], customer["username"])
        )
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
        cur = conn.cursor()
        cur.execute("DELETE FROM customers WHERE username = %s;", (username,))
        conn.commit()
        message["status"] = "Customer deleted successfully."
    except: 
        conn.rollback()
        message["status"] = "Cannot delete customer" 
    finally:
        conn.close()
    return message

#create_customers_table()
#print(insert_customer(customer_Sara))
#print(insert_customer(customer_Malak))
#print(get_customer_by_username("MalakS"))
#print(get_customers())
#print(delete_customer("MalakS"))
customer_Sara = {
    "full_name": "Sara Abbas",
    "username": "SaraA", 
    "password": "passwordSara",
    "address": "Geneva, Switzerland",
    "age": 22,
    "gender": "Female",
    "marital_status": "Single",
    "wallet_balance": 1000.0
}
#print(update_customer(customer_Sara))

def create_inventory_table():
    """Create the 'inventory' table in the database if it does not exist.
    """
    try:

        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS inventory(
                 good_id SERIAL PRIMARY KEY,
                 name TEXT UNIQUE NOT NULL,
                 category TEXT NOT NULL,
                 price INT NOT NULL,
                 description TEXT,
                 count INT
            );
        ''')
        conn.commit()
        print("Customer table created successfully!")
    except psycopg2.Error as e:
        print(f"Error creating 'customers' table: {e}")
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
        cur.execute("INSERT INTO inventory(name, category, price, description, count) VALUES (%s, %s, %s, %s, %s) RETURNING good_id",
                    (good['name'], good['category'], good['price'], good['description'], good['count'])) 
        inserted_good_id = cur.fetchone()[0]
        conn.commit()
        inserted_good = get_good_by_good_id(inserted_good_id)

    except psycopg2.Error as e: 
        print(f"Error inserting good: {e}")
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
        cur = conn.cursor() 
        cur.execute("SELECT * FROM inventory") 
        rows = cur.fetchall()
        
        for i in rows:
            good = {}
            good["good_id"] = i[0] 
            good["name"] = i[1] 
            good["category"] = i[2] 
            good["price"] = i[3] 
            good["description"] = i[4] 
            good["count"] = i[5]
            goods.append(good)

    except psycopg2.Error as e:
        print(f"Error fetching customers: {e}")
    finally:
        conn.close()
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
        cur = conn.cursor()
        cur.execute("SELECT * FROM inventory WHERE good_id = %s", (good_id,)) 
        row = cur.fetchone()
        
        if row:
            good["good_id"] = row[0] 
            good["name"] = row[1] 
            good["category"] = row[2] 
            good["price"] = row[3] 
            good["description"] = row[4] 
            good["count"] = row[5]

    except psycopg2.Error as e:
        print(f"Error fetching customers: {e}")
    finally:
        conn.close()
    return good

def update_good(good): 
    """Update good information in the database.

    :param good: A dictionary representing the updated good information
    :type good: dict
    :return: A dictionary representing the updated good
    :rtype: dict
    """
    updated_good = {} 
    good_info = get_good_by_name(good['name'])
    good_id = good_info['good_id']
    try:
        conn = connect_to_db() 
        cur = conn.cursor()
        cur.execute("UPDATE inventory SET name = %s , category = %s, price = %s, description = %s, count = %s WHERE good_id = %s",
                    (good['name'], good['category'], good['price'], good['description'], good['count'], good_id))
        conn.commit()
        updated_good = get_good_by_name(good['name'])
    except psycopg2.Error as e:
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
        cur = conn.cursor()
        cur.execute("DELETE from inventory WHERE good_id = %s", (good_id,))
        conn.commit()
        message["status"] = "Good deleted successfully."
    except psycopg2.Error as e:
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
        cur = conn.cursor()
        cur.execute("SELECT * FROM inventory WHERE name = %s", (name,)) 
        row = cur.fetchone()
        
        if row:
            good["good_id"] = row[0] 
            good["name"] = row[1] 
            good["category"] = row[2] 
            good["price"] = row[3] 
            good["description"] = row[4] 
            good["count"] = row[5]
    except psycopg2.Error as e:
        good = {}
    return good

#create_inventory_table()
#print(insert_good(ahmad_tea))
#print(insert_good(dollys))
#print(get_good_by_good_id(5))
#print(get_goods())
#print(delete_good(3))
#print(get_good_by_name("Ahmad Tea"))
dollys_updated = {
    "name": "Dolly's Ketchup",
    "category": "Food", 
    "price": 2.0,
    "description": "Tomato Ketchup",
    "count": 200
}
#print(update_good(dollys_updated))

def create_purchases_table():
    """Create the 'purchases' table in the database if it does not exist.
    """
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS historical_purchases(
                 hist_purchase_id SERIAL PRIMARY KEY,
                 customer_username TEXT NOT NULL ,
                 good_name TEXT NOT NULL,
                 price REAL NOT NULL,
                 purchase_date TIMESTAMP,
                 FOREIGN KEY (customer_username) REFERENCES customers(username),
                 FOREIGN KEY (good_name) REFERENCES inventory(name)
            );
        ''')
        conn.commit()
        print("Historical Purchases table created successfully!")
    except psycopg2.Error as e:
        print(f"Error creating 'customers' table: {e}")
    finally:
        conn.close()

def get_purchases_by_username(customer_username): 
    """Retrieve customer historical purchases based on the provided username.

    :param username: The username of the customer
    :type username: str
    :return: A list representing all the purchases made by a customer if found, else None
    :rtype: list or None
    """
    purchases = []
    try:
        conn = connect_to_db() 
        cur = conn.cursor()
        cur.execute("SELECT * FROM historical_purchases WHERE customer_username = %s", (customer_username,)) 
        rows = cur.fetchall()
        
        # convert row object to dictionary 
        for row in rows:
            purchase = {
                "customer_username": row[1],
                "good_name": row[2],
                "price": row[3],
                "date": row[4]
            }
            purchases.append(purchase)
    except:
        purchases = []
    conn.close()
    return purchases

def insert_purchase(customer_username, good_name, price): 
    """Insert a new purchase into the database.

    :param customer: A dictionary representing the customer
    :type customer: dict
    :return: A dictionary representing the inserted customer
    :rtype: dict
    """
    inserted_purchase = {} 
    datetoday = date.today()
    current_time = datetime.now().time()
    combined_datetime = datetime.combine(datetoday, current_time)
    formatted_datetime = combined_datetime.strftime("%Y-%m-%d %H:%M:%S")
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO historical_purchases (customer_username, good_name, price, purchase_date) VALUES (%s, %s, %s, %s)",
                    (customer_username, good_name, price, formatted_datetime))
        conn.commit()

        cur.execute("SELECT * FROM historical_purchases WHERE customer_username = %s ORDER BY purchase_date DESC LIMIT 1", (customer_username,))
        row = cur.fetchone()

        if row:
            inserted_purchase["customer_username"] = row[1]
            inserted_purchase["good_name"] = row[2]
            inserted_purchase["price"] = row[3]
            inserted_purchase["purchase_date"] = row[4].strftime("%Y-%m-%d %H:%M:%S")
        
    except psycopg2.Error as e:
        conn.rollback()
        return {'error': f'Error: {str(e)}. The username must be unique.'}
    finally: 
        conn.close()
    return inserted_purchase

def delete_latest_purchase(customer_username):
    """Delete the latest purchase from the database.

    :param customer_username: A string representing the customer's user name
    :type customer: string
    :return: A dictionary representing the deleted purchase
    :rtype: dict
    """
    deleted_purchase = {} 
    try:
        conn = connect_to_db()
        cur = conn.cursor()

        cur.execute("SELECT * FROM historical_purchases WHERE customer_username = %s ORDER BY purchase_date DESC LIMIT 1", (customer_username,))
        row = cur.fetchone()

        if row:
            deleted_purchase["customer_username"] = row[1]
            deleted_purchase["good_name"] = row[2]
            deleted_purchase["price"] = row[3]
            deleted_purchase["purchase_date"] = row[4].strftime("%Y-%m-%d %H:%M:%S")

        cur.execute("DELETE FROM historical_purchases WHERE hist_purchase_id = %s", (row[0],))
        conn.commit()
        
    except psycopg2.Error as e:
        conn.rollback()
        return {'error': f'Error: {str(e)}. The username must be unique.'}
    finally: 
        conn.close()
    return deleted_purchase

def drop_purchases_table():
    """Drop the 'historical_purchases' table from the database.
    """
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("DROP TABLE IF EXISTS historical_purchases")
        conn.commit()
        print("Historical Purchases table dropped successfully!")
    except Exception as e:
        print(f"Error dropping table: {str(e)}")
    finally:
        conn.close()

# Call the function to drop the table
create_purchases_table()
#print(insert_purchase('SaraA','Ahmad Tea', 10))
#print(delete_latest_purchase('SaraA'))
#print(get_purchases_by_username('SaraA'))
#drop_purchases_table()