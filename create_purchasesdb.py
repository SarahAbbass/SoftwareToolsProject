import sqlite3
from create_db import connect_to_db
from datetime import datetime


def create_purchases_table():
    """Create the 'purchases' table in the database if it does not exist.
    """
    try:
        conn = connect_to_db()
        conn.execute('''
            CREATE TABLE IF NOT EXISTS historical_purchases(
                 hist_purchase_id INTEGER PRIMARY KEY AUTOINCREMENT,
                 customer_username TEXT NOT NULL ,
                 good_name TEXT NOT NULL,
                 price REAL NOT NULL,
                 purchase_date TEXT CHECK (purchase_date LIKE '____-__-__ __:__:__'),
                 FOREIGN KEY (customer_username) REFERENCES customers(username)
            );
        ''')
        conn.commit()
        print("Historical Purchases table created successfully!")
    except:
        print("Historical Purchases table creation failed -")
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
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM historical_purchases WHERE customer_username = ?", (customer_username,)) 
        rows = cur.fetchall()
        
        # convert row object to dictionary 
        for row in rows:
            purchase = {
                "customer_username": row["customer_username"],
                "good_name": row["good_name"],
                "price": row["price"],
                "date": row["purchase_date"]
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
    current_datetime = datetime.now()
    # Convert the current datetime to a string in the required format
    purchase_date = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO historical_purchases (customer_username, good_name, price, purchase_date) VALUES (?, ?, ?, ?)",
                    (customer_username, good_name, price, purchase_date))
        conn.commit()

        cur.execute("SELECT * FROM historical_purchases WHERE customer_username = ? ORDER BY datetime(purchase_date) DESC LIMIT 1", (customer_username,))
        row = cur.fetchone()

        if row:
            # Access the elements by index
            inserted_purchase["customer_username"] = row[1]
            inserted_purchase["good_name"] = row[2]
            inserted_purchase["price"] = row[3]
            inserted_purchase["purchase_date"] = row[4]
        
    except sqlite3.IntegrityError as e:
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

        cur.execute("SELECT * FROM historical_purchases WHERE customer_username = ? ORDER BY datetime(purchase_date) DESC LIMIT 1", (customer_username,))
        row = cur.fetchone()

        if row:
            deleted_purchase["customer_username"] = row[1]
            deleted_purchase["good_name"] = row[2]
            deleted_purchase["price"] = row[3]
            deleted_purchase["purchase_date"] = row[4]

            cur.execute("DELETE FROM historical_purchases WHERE hist_purchase_id = ?", (row[0],))
            conn.commit()
        
    except sqlite3.IntegrityError as e:
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
user_test = "user_test"
good_test = "user_good"
#create_purchases_table()
#print(insert_purchase(user_test, good_test, 10))
#print(delete_latest_purchase("user_test"))
#print(get_purchases_by_username(user_test))