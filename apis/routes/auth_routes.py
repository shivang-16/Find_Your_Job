from flask import Blueprint, request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from functions.jwt_token import encode_token
import uuid
from pymongo.errors import DuplicateKeyError
from db.db import get_collection
from functions.insert_job import collection

auth_blueprint = Blueprint('auth', __name__)

users_collection = get_collection("users")

@auth_blueprint.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if users_collection.find_one({"username": username}):
        return jsonify({'message': 'User already exists!'}), 400

    hashed_password = generate_password_hash(password, method='sha256')
    user_id = str(uuid.uuid4())

    try:
        users_collection.insert_one({
            "_id": user_id,
            "username": username,
            "password": hashed_password
        })
        return jsonify({'message': 'User registered successfully!'}), 201
    except DuplicateKeyError:
        return jsonify({'message': 'User already exists!'}), 400
    except Exception as e:
        return jsonify({'message': 'An error occurred while registering the user.'}), 500

@auth_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = users_collection.find_one({"username": username})

    if not user or not check_password_hash(user['password'], password):
        return jsonify({'message': 'Invalid credentials!'}), 401

    token = encode_token(user['_id'])

    response = make_response(jsonify({'message': 'Login successful!'}))
    response.set_cookie('token', token)

    return response
