from flask import jsonify, request, render_template
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from flask_mail import Message
from . import user
from ..models import User
from .. import db
from .. import mail
import random, string

def random_name(n):
   rand_list = [random.choice(string.ascii_letters + string.digits) for i in range(n)]
   return ''.join(rand_list)

@user.route("/info", methods=['GET'])
@jwt_required
def show_info():
    current_user = User.query.filter_by(email=get_jwt_identity()).first()
    return jsonify({
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email
    }), 200

@user.route("/create", methods=['POST'])
def create():
    if not request.get_json():
        return jsonify({"msg": "Missing JSON in request"}), 400
    username = request.get_json()["username"]
    email = request.get_json()["email"]
    password = request.get_json()["password"]
    if not username:
        return jsonify({"msg": "Missing username parameter."}), 400
    if not email:
        return jsonify({"msg": "Missing email parameter."}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter."}), 400
    if User.query.filter_by(email=email).first() is not None:
        return jsonify({"msg": "This email has been used."}), 400
    new_user = User(username=username, email=email, password=password)
    new_user.given_activation_token = random_name(128)
    new_user.given_activation_token_date = datetime.utcnow()
    db.session.add(new_user)
    db.session.commit()

    #mail送信
    msg = Message("Activate your Account", sender="e1833@s.akashi.ac.jp", recipients=[new_user.email])
    msg.body = "Activation"
    msg.html = f"<a>http://127.0.0.1:5000/api/users/activate/{new_user.email}/{new_user.given_activation_token}</a>"
    mail.send(msg)

    return jsonify({"msg": "create user successfully."}), 200

@jwt_required
@user.route("/send_mail_to activate", methods=['GET'])
def send_mail():
    if request.get_json():
        current_user = User.query.filter_by(email=get_jwt_identity()).first()
        if current_user.is_valid:
            return jsonify({"msg": "Your Account is already valid"}), 400
        current_user.given_activation_token = random_name(128)
        current_user.given_activation_token_date = datetime.utcnow()
        db.session.add(current_user)
        db.session.commit()

        msg = Message("Activate your Account", sender="e1833@s.akashi.ac.jp", recipients=[new_user.email])
        msg.body = "Activation"
        msg.html = f"<a>http://127.0.0.1:5000/api/users/activate/{new_user.mail}/{new_user.given_activation_token}</a>"
        mail.send(msg)

        return jsonify({"msg": "I sent you a activation mail."}), 200

@user.route("/activate/<email>/<activation_token>", methods=['GET'])
def to_valid(email, activation_token):
    user = User.query.filter_by(email=email).first()
    if user is None:
        return jsonify({"msg": "Invalid email"})
    if user.given_activation_token != activation_token:
        return jsonify({"msg": "Invalid token"})
    if (datetime.utcnow() - user.given_activation_token_date).seconds > 1800:
        return jsonify({"msg": "This token is expired"})
    user.is_valid = True
    db.session.add(user)
    db.session.commit()
    return jsonify({"msg": "Your account becomes valid."})
