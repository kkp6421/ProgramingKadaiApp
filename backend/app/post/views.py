from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from . import post
from .. import db
from ..models import User, Post


@post.route("/", methods=['GET'])
@jwt_required
def index():
    current_user = User.query.filter_by(email=get_jwt_identity()).first()
    if not current_user.is_valid:
        return jsonify({"msg": "Your Account isn't invalid"}), 400
    all_posts = User.query.all()
    return jsonify([{
        "id": x.id,
        "text": x.text,
        "post_date": x.post_date,
        "user_id": x.user_id
    } for x in all_posts]), 200


@post.route("/create", methods=['POST'])
@jwt_required
def create():
    if request.get_json():
        current_user = User.query.filter_by(email=get_jwt_identity()).first()
        if not current_user.is_valid:
            return jsonify({"msg": "Your Account isn't invalid"}), 400
        text = request.get_json()["text"]
        if not text:
            return jsonify({"msg": "Missing text parameter"}), 400
        new_post = Post(text=text)
        current_user.posts.append(new_post)
        db.session.add(current_user)
        db.session.commit()
        return jsonify({"msg": "Create task successfully."}), 200

@post.route("/delete", methods=['POST'])
@jwt_required
def delete():
    if request.get_json():
        current_user = User.query.filter_by(email=get_jwt_identity()).first()
        if not current_user.is_valid:
            return jsonify({"msg": "Your Account isn't invalid"}), 400
        post_id = request.get_json()["post_id"]
        if not post_id:
            return jsonify({"msg": "Missing post_id parameter"}), 400
        post = Post.query.filter_by(id=post_id).first()
        if not current_user.id == post.user_id:
            return jsonify({"msg": "you don't have the authority."}), 400
        db.session.delete(post)
        db.session.commit()
        return jsonify({"msg": "Delete task successfully."}), 200