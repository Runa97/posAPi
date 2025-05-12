from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User
from app import db
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')

    if not username or not password or not role:
        return jsonify({"msg": "Missing fields"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"msg": "User already exists"}), 409

    hashed_pw = generate_password_hash(password)
    user = User(username=username, password=hashed_pw, role=role)
    db.session.add(user)
    db.session.commit()

    return jsonify({"msg": "User registered successfully"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        token = create_access_token(identity={"id": user.id, "role": user.role})
        return jsonify({"token": token}), 200

    return jsonify({"msg": "Invalid credentials"}), 401

