from flask_jwt_extended import create_access_token, decode_token, get_jwt_identity
from datetime import timedelta
from app import jwt

# Create an access token
def create_jwt_token(identity):
    """
    Create an access token for a given identity (user).
    """
    access_token = create_access_token(
        identity=identity, 
        expires_delta=timedelta(days=1)  # Token expires in 1 day
    )
    return access_token

# Decode a token and return the identity (user information)
def decode_jwt_token(token):
    """
    Decode the JWT token and retrieve identity (user).
    """
    decoded_token = decode_token(token)
    return decoded_token

# Get current user's identity from the token
def get_current_user_identity():
    """
    Get the current user's identity (user ID or other relevant details) from the JWT token.
    """
    return get_jwt_identity()
