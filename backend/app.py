from flask import Flask, request, jsonify, make_response
import mysql.connector
import jwt
import datetime
import uuid
from flask_cors import CORS, cross_origin


app = Flask(__name__)
# CORS(app, supports_credentials=True)
# CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
CORS(app, supports_credentials=True, origins=['http://localhost:3000', 'http://127.0.0.1:9000'])
# CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
# CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}}, supports_credentials=True)

SECRET_KEY = '_ASDGlZL-7iu8cu55x6klmdLIh4NFKtNTv0kuEaZ8uA='

# Replace these values with your actual database connection details
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
        return conn
    except mysql.connector.Error as e:
        print(f"Error connecting to MariaDB: {e}")
        return None



@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE, OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')

    # Allow requests from both frontend origin and backend origin
    request_origin = request.headers.get('Origin')
    allowed_origins = ['http://localhost:3000', 'http://127.0.0.1:9000']
    if request_origin in allowed_origins:
        response.headers['Access-Control-Allow-Origin'] = request_origin

    # Set the HTTP status code to 200 OK
    response.status_code = 200

    return response



# Register a before_request hook to validate the token before each request
@app.before_request
def before_request():
    # Skip token validation for signup and login routes
    if request.endpoint in ['create_account', 'login']:
        return

    # Get the token from the 'Authorization' header
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({'message': 'Token is missing'}), 401

    try:
        # Extract the token from the header (Bearer token)
        token = auth_header.split()[1]

        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        # Check token expiration
        if datetime.datetime.utcnow() >= datetime.datetime.fromtimestamp(decoded_token['exp']):
            return jsonify({'message': 'Token has expired'}), 401
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token has expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token'}), 401


# User registration route
@app.route('/create_account', methods=['POST', 'OPTIONS'])
def create_account():
    # Extract user information from the request
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    # Validate required fields
    if not name or not email or not password:
        return jsonify({'message': 'Name, Email, and Password are required'}), 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Check if the email is already registered
        cur.execute("SELECT id FROM users WHERE email = %s", (email,))
        user_id = cur.fetchone()

        if user_id:
            return jsonify({'message': 'Email already registered'}), 409

        # Generate a UUID for the user
        user_uuid = str(uuid.uuid4())

        # Hash the password before storing it in the database
        # Make sure to use a secure hashing algorithm like bcrypt
        hashed_password = password  # Replace this with the actual hash

        # Insert the user information into the database with the UUID
        cur.execute("INSERT INTO users (id, name, email, password) VALUES (%s, %s, %s, %s)", (user_uuid, name, email, hashed_password))
        conn.commit()

        return jsonify({'message': 'Account created successfully', 'user_id': user_uuid}), 201

    except mysql.connector.Error as e:
        print(f"Database error: {e}")
        return jsonify({'message': 'Failed to create account'}), 500

    finally:
        if conn:
            conn.close()

# User login route
@app.route('/login', methods=['POST', 'OPTIONS'])
# @cross_origin(supports_credentials=True)
def login():
    # Extract user credentials from the request
    print("login---------------------------------")
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

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

            # Create an HTTP response with the token in cookies
            response = make_response(jsonify({'token': token, 'message': 'Login successful'}), 200)
            # Set Access-Control-Allow-Origin to *
            response.headers['Access-Control-Allow-Origin'] = '*'

            return response

        return jsonify({'message': 'Invalid email or password'}), 401

    except mysql.connector.Error as e:
        print(f"Database error: {e}")
        return jsonify({'message': 'Failed to login'}), 500

    finally:
        if conn:
            conn.close()

# Route to get all password entries for a specific user
@app.route('/get_all_passwords', methods=['GET', 'OPTIONS'])
# @cross_origin(supports_credentials=True)
def get_all_passwords():
    # if request.method == 'OPTIONS':
    #     # This is the preflight request, so just return the CORS headers.
    #     response = make_response()
    #     response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
    #     response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
    #     response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    #     response.headers.add('Access-Control-Allow-Credentials', 'true')
    #     return response
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        user_id = get_user_id_from_token()

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

        return jsonify(password_list), 200

    except mysql.connector.Error as e:
        print(f"Database error: {e}")
        return jsonify({'message': 'Failed to retrieve password entries'}), 500

    finally:
        if conn:
            conn.close()


# Route to create a new password entry
@app.route('/create_password', methods=['POST', 'OPTIONS'])
def create_password():
    # Extract password information from the request
    data = request.get_json()
    platform_name = data.get('platform_name')
    account_name = data.get('account_name')
    password = data.get('password')

    # Validate required fields
    if not platform_name or not account_name or not password:
        return jsonify({'message': 'Platform Name, Account Name, and Password are required'}), 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Generate a UUID for password
        ps_id = str(uuid.uuid4())
        user_id = get_user_id_from_token()  # Get the user ID separately

        # Insert the password information into the database
        cur.execute("INSERT INTO passwords (id, user_id, platform_name, account_name, password) VALUES (%s, %s, %s, %s, %s)",
                    (ps_id, user_id, platform_name, account_name, password))
        conn.commit()
        return jsonify({'message': 'Password entry created successfully'}), 201

    except mysql.connector.Error as e:
        print(f"Database error: {e}")
        return jsonify({'message': 'Failed to create password entry'}), 500

    finally:
        if conn:
            conn.close()


# Route to update an existing password entry
@app.route('/update_password', methods=['PUT'])
def update_password():
    # Extract password information from the request
    data = request.get_json()
       # Extract password_id from query parameters in the URL
    password_id = request.args.get('password_id')
    platform_name = data.get('platform_name')
    account_name = data.get('account_name')
    password = data.get('password')

    print("pqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq", password_id, platform_name, account_name, password )

    # Validate required fields
    if not password_id or not platform_name or not account_name or not password:
        return jsonify({'message': 'Password ID, Platform Name, Account Name, and Password are required'}), 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Check if the password entry exists
        cur.execute("SELECT id FROM passwords WHERE id = %s", (password_id,))
        password_entry = cur.fetchone()

        if not password_entry:
            return jsonify({'message': 'Password entry not found'}), 404

        # Update the password entry in the database
        cur.execute("UPDATE passwords SET platform_name = %s, account_name = %s, password = %s WHERE id = %s",
                    (platform_name, account_name, password, password_id))
        conn.commit()

        return jsonify({'message': 'Password entry updated successfully'}), 200

    except mysql.connector.Error as e:
        print(f"Database error: {e}")
        return jsonify({'message': 'Failed to update password entry'}), 500

    finally:
        if conn:
            conn.close()


# Route to delete an existing password entry
@app.route('/delete_password/', methods=['DELETE'])
def delete_password():
    try:
        # Extract password_id from query parameters in the URL
        password_id = request.args.get('password_id')
        conn = get_db_connection()
        cur = conn.cursor()

        # Check if the password entry exists
        cur.execute("SELECT id FROM passwords WHERE id = %s AND user_id = %s", (password_id, get_user_id_from_token()))
        password_entry = cur.fetchone()

        if not password_entry:
            return jsonify({'message': 'Password entry not found'}), 404

        # Delete the password entry from the database
        cur.execute("DELETE FROM passwords WHERE id = %s", (password_id,))
        conn.commit()

        return jsonify({'message': 'Password entry deleted successfully'}), 200

    except mysql.connector.Error as e:
        print(f"Database error: {e}")
        return jsonify({'message': 'Failed to delete password entry'}), 500

    finally:
        if conn:
            conn.close()
# Helper function to get user ID from token
def get_user_id_from_token():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return None

    try:
        # Extract the token from the header (Bearer token)
        token = auth_header.split()[1]
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        print("---------------------------", decoded_token['user_id'])
        return decoded_token['user_id']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True, port=9000)
