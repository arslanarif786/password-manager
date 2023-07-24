import mysql.connector
import jwt
import datetime
import uuid
SECRET_KEY = '_ASDGlZL-7iu8cu55x6klmdLIh4NFKtNTv0kuEaZ8uA='

# Define your SECRET_KEY, DB_HOST, DB_USER, DB_PASSWORD, and DB_NAME here
DB_HOST = '192.168.10.17'
DB_USER = 'test'
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
        return conn
    except mysql.connector.Error as e:
        print(f"Error connecting to MariaDB: {e}")
        return None

# User registration function
def create_account(name, email, password):
    if not name or not email or not password:
        return {'message': 'Name, Email, and Password are required'}, 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Check if the email is already registered
        cur.execute("SELECT id FROM users WHERE email = %s", (email,))
        user_id = cur.fetchone()

        if user_id:
            return {'message': 'Email already registered'}, 409

        # Generate a UUID for the user
        user_uuid = str(uuid.uuid4())

        # Hash the password before storing it in the database
        # Make sure to use a secure hashing algorithm like bcrypt
        hashed_password = password  # Replace this with the actual hash

        # Insert the user information into the database with the UUID
        cur.execute("INSERT INTO users (id, name, email, password) VALUES (%s, %s, %s, %s)", (user_uuid, name, email, hashed_password))
        conn.commit()

        return {'message': 'Account created successfully', 'user_id': user_uuid}, 201

    except mysql.connector.Error as e:
        print(f"Database error: {e}")
        return {'message': 'Failed to create account'}, 500

    finally:
        if conn:
            conn.close()

# User login function
def login(email, password):
    if not email or not password:
        return {'message': 'Email and Password are required'}, 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Fetch the user from the database based on the provided email
        cur.execute("SELECT id, name, password FROM users WHERE email = %s", (email,))
        user = cur.fetchone()

        if user and user[2] == password:
            # Generate a JWT token
            token_payload = {
                'email': email,
                'user_id': user[0],
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)  # Token expiration (1 day in this example)
            }
            token = jwt.encode(token_payload, SECRET_KEY, algorithm='HS256')

            return {'token': token, 'message': 'Login successful'}, 200

        return {'message': 'Invalid email or password'}, 401

    except mysql.connector.Error as e:
        print(f"Database error: {e}")
        return {'message': 'Failed to login'}, 500

    finally:
        if conn:
            conn.close()
