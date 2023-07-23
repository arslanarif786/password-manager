import mysql.connector
import uuid

DB_HOST = '192.168.100.38'
DB_USER = 'test2'
DB_PASSWORD = '123'
DB_NAME = 'password manager'

# Database connection setup
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        print("Database connection established successfully.")  # Add this line for debugging
        return conn
    except mysql.connector.Error as e:
        print(f"Error connecting to MariaDB: {e}")
        return None
    
def create_password(user_id, platform_name, account_name, password):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Generate a UUID for the password entry
        password_id = str(uuid.uuid4())

        # Insert the password information into the database
        query = "INSERT INTO passwords (id, user_id, platform_name, account_name, password) VALUES (%s, %s, %s, %s, %s)"
        data = (password_id, user_id, platform_name, account_name, password)
        cur.execute(query, data)
        conn.commit()

        return {'message': 'Password entry created successfully'}, 201

    except mysql.connector.Error as e:
        print(f"Database error: {e}")
        return {'message': 'Failed to create password entry'}, 500

    finally:
        if conn:
            conn.close()


# Function to update an existing password entry
def update_password(password_id, platform_name, account_name, password):
    if not password_id or not platform_name or not account_name or not password:
        return {'message': 'Password ID, Platform Name, Account Name, and Password are required'}, 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Check if the password entry exists
        cur.execute("SELECT id FROM passwords WHERE id = %s", (password_id,))
        password_entry = cur.fetchone()

        if not password_entry:
            return {'message': 'Password entry not found'}, 404

        # Update the password entry in the database
        cur.execute("UPDATE passwords SET platform_name = %s, account_name = %s, password = %s WHERE id = %s",
                    (platform_name, account_name, password, password_id))
        conn.commit()

        return {'message': 'Password entry updated successfully'}, 200

    except mysql.connector.Error as e:
        print(f"Database error: {e}")
        return {'message': 'Failed to update password entry'}, 500

    finally:
        if conn:
            conn.close()

# Function to get all password entries for a specific user
def get_passwords_for_user(user_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Fetch all password entries for the user from the database
        cur.execute("SELECT id, platform_name, account_name, password FROM passwords WHERE user_id = %s", (user_id,))
        password_entries = cur.fetchall()

        # Create a list of password dictionaries
        password_list = []
        for entry in password_entries:
            password_dict = {
                'password_id': entry[0],
                'platform_name': entry[1],
                'account_name': entry[2],
                'password': entry[3]
            }
            password_list.append(password_dict)

        return {'passwords': password_list}, 200

    except mysql.connector.Error as e:
        print(f"Database error: {e}")
        return {'message': 'Failed to retrieve password entries'}, 500

    finally:
        if conn:
            conn.close()    
# Function to delete an existing password entry
def delete_password(password_id, user_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Check if the password entry exists for the given user_id
        cur.execute("SELECT id FROM passwords WHERE id = %s AND user_id = %s", (password_id, user_id))
        password_entry = cur.fetchone()

        if not password_entry:
            return {'message': 'Password entry not found'}, 404

        # Delete the password entry from the database
        cur.execute("DELETE FROM passwords WHERE id = %s", (password_id,))
        conn.commit()

        return {'message': 'Password entry deleted successfully'}, 200

    except mysql.connector.Error as e:
        print(f"Database error: {e}")
        return {'message': 'Failed to delete password entry'}, 500

    finally:
        if conn:
            conn.close()
                   
