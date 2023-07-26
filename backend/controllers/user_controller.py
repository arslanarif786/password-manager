from flask import request, jsonify, Blueprint
from models.auth_model import create_account, login

# Define routes in a Blueprint
user_routes = Blueprint('user_routes', __name__)

# Route for user registration
@user_routes.route('/create_account', methods=['POST', 'OPTIONS'])
def create_account_controller():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    result, status_code = create_account(name, email, password)
    return jsonify(result), status_code

# Route for user login
@user_routes.route('/login', methods=['POST', 'OPTIONS'])
def login_controller():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    result, status_code = login(email, password)
    return jsonify(result), status_code

# After request hook for CORS headers
@user_routes.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE, OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')

    # Allow requests from both frontend origin and backend origin
    request_origin = request.headers.get('Origin')
    response.headers['Access-Control-Allow-Origin'] = request_origin
    # Set the HTTP status code to 200 OK
    response.status_code = 200

    return response
