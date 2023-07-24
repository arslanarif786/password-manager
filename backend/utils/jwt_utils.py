import jwt

# Helper function to get user ID from token
SECRET_KEY = '_ASDGlZL-7iu8cu55x6klmdLIh4NFKtNTv0kuEaZ8uA='
def get_user_id_from_token(auth_header):
    if not auth_header:
        return None

    try:
        # Extract the token from the header (Bearer token)
        token = auth_header.split()[1]
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return decoded_token['user_id']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
    
