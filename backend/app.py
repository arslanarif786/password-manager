from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=['http://localhost:3000', 'http://127.0.0.1:7000'], supports_credentials=True)

# Import specific functions from models and controllers
from models.auth_model import create_account, login
from models.password_model import get_passwords_for_user, create_password, update_password, delete_password
from controllers.user_controller import user_routes
from controllers.password_controller import password_routes

app.register_blueprint(user_routes)
app.register_blueprint(password_routes)

# Register route handlers
app.route('/create_account', methods=['POST'])(create_account)
app.route('/login', methods=['POST'])(login)
app.route('/get_all_passwords', methods=['GET'])(get_passwords_for_user)
app.route('/create_password', methods=['POST'])(create_password)
app.route('/update_password', methods=['PUT'])(update_password)
app.route('/delete_password/', methods=['DELETE'])(delete_password)

if __name__ == '__main__':
    app.run(debug=True, port=7000)