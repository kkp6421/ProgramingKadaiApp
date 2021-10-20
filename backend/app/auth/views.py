from flask import request, jsonify
from . import auth
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from ..models import User

@auth.route("/api/auth", methods=['POST'])
def login():
    if not request.get_json():
        return jsonify({"msg": "Missing JSON in request"}), 400
    email = request.get_json()["email"]
    password = request.get_json()["password"]
    if not email:
        return jsonify({"msg": "Missing email parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400
    user = User.query.filter_by(email=email).first()
    if user is None or not user.verify_password(password):
        return jsonify({"msg": "Invalid email or password"}), 401
    if not user.is_valid:
        return jsonify({"msg": "Your Account isn't invalid"}), 400
    print("OK")
    access_token = create_access_token(identity=email)
    return jsonify({"msg": "login Success!", "token": access_token}), 200


@auth.route("/api/protected")
@jwt_required
def protected():
    current_user = User.query.filter_by(email=get_jwt_identity()).first()
    return jsonify({
        "id": current_user.id,
        "email": current_user.email,
        "username": current_user.username
    }), 200