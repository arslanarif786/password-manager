from flask import request, jsonify, Blueprint
from models.password_model import create_password, update_password, get_passwords_for_user, delete_password
from utils.jwt_utils import get_user_id_from_token

# Define routes in a Blueprint
password_routes = Blueprint('password_routes', __name__)


# Before request hook for token validation
@password_routes.before_request
def before_request():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({'message': 'Token is missing'}), 401

    decoded_token = get_user_id_from_token(auth_header)
    if not decoded_token:
        return jsonify({'message': 'Invalid token'}), 401

        # You can access decoded_token['user_id'] here if needed for further processing.

# Route to get all password entries for a specific user
@password_routes.route('/get_all_passwords', methods=['GET', 'OPTIONS'])
def get_all_passwords():
    try:
        user_id = get_user_id_from_token(request.headers.get('Authorization'))
        if not user_id:
            return jsonify({'message': 'Token is missing or invalid'}), 401

        result, status_code = get_passwords_for_user(user_id)
        return jsonify(result), status_code

    except Exception as e:
        return jsonify({'message': 'Failed to retrieve password entries', 'error': str(e)}), 500


# Route to create a new password entry
@password_routes.route('/create_password', methods=['POST', 'OPTIONS'])
def create_password_controller():
    try:
        data = request.get_json()
        platform_name = data.get('platform')  # Corrected key name
        account_name = data.get('username')    # Corrected key name
        password = data.get('password')

        if not platform_name or not account_name or not password:
            return jsonify({'message': 'Platform Name, Account Name, and Password are required'}), 400

        user_id = get_user_id_from_token(request.headers.get('Authorization'))
        if not user_id:
            return jsonify({'message': 'Token is missing or invalid'}), 401

        result, status_code = create_password(user_id, platform_name, account_name, password)
        return jsonify(result), status_code

    except Exception as e:
        return jsonify({'message': 'Failed to create password entry', 'error': str(e)}), 500


# Route to update an existing password entry
@password_routes.route('/update_password/', methods=['PUT', 'OPTIONS'])
def update_password_controller():
    data = request.get_json()
    password_id = request.args.get('password_id')
    platform_name = data.get('platform')
    account_name = data.get('username')
    password = data.get('password')

    user_id = get_user_id_from_token(request.headers.get('Authorization'))
    if not user_id:
        return jsonify({'message': 'Token is missing or invalid'}), 401

    result, status_code = update_password(password_id, platform_name, account_name, password)
    return jsonify(result), status_code


# Route to delete an existing password entry
@password_routes.route('/delete_password/', methods=['DELETE'])
def delete_password_controller():
    try:
        password_id = request.args.get('password_id')
        user_id = get_user_id_from_token(request.headers.get('Authorization'))
        if not user_id:
            return jsonify({'message': 'Token is missing or invalid'}), 401

        result, status_code = delete_password(password_id, user_id)
        return jsonify(result), status_code

    except Exception as e:
        return jsonify({'message': 'Failed to delete password entry', 'error': str(e)}), 500
    

# After request hook for CORS and response modifications
@password_routes.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE, OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')

    # Allow requests from both frontend origin and backend origin
    request_origin = request.headers.get('Origin')
    allowed_origins = ['http://localhost:3000', 'http://127.0.0.1:7000']
    if request_origin in allowed_origins:
        response.headers['Access-Control-Allow-Origin'] = request_origin

    # Set the HTTP status code to 200 OK
    response.status_code = 200

    return response


