from functools import wraps
from flask import request, jsonify
from functions.jwt_token import decode_token


def check_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.cookies.get('token')

        if not token:
            return jsonify({'message': 'Token is missing!'}), 403

        user_id = decode_token(token)
        if isinstance(user_id, str):  # This means an error message was returned instead of the user_id
            return jsonify({'message': user_id}), 403

        return f(user_id, *args, **kwargs)

    return decorated_function
