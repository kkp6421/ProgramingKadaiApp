from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from . import comment
from .. import db
from ..models import User, Comment, Post


@comment.route("/my_comments", methods=['GET'])
@jwt_required
def index():
    current_user = User.query.filter_by(email=get_jwt_identity()).first()
    if not current_user.is_valid:
        return jsonify({"msg": "Your Account isn't invalid"}), 400
    all_my_commments = current_user.comments
    return jsonify([{
        "id": x.id,
        "text": x.text,
        "comment_date": x.comment_date,
        "user_id": x.user_id,
        "post_id": x.post_id,
        "post_text": Post.query.filter_by(id=x.post_id).first().text
    } for x in all_my_commments]), 200


@comment.route("/create", methods=['POST'])
@jwt_required
def create():
    if request.get_json():
        current_user = User.query.filter_by(email=get_jwt_identity()).first()
        if not current_user.is_valid:
            return jsonify({"msg": "Your Account isn't invalid"}), 400
        text = request.get_json()["text"]
        post_id = request.get_json()["post_id"]
        if not text:
            return jsonify({"msg": "Missing text parameter"}), 400
        if not post_id:
            return jsonify({"msg": "Missing selected_post_id parameter"}), 400
        new_comment = Comment(text=text)
        post = Post.query.filter_by(id=post_id).first()
        post.comments.append(new_comment)
        current_user.comments.append(new_comment)
        db.session.add(current_user)
        db.session.commit()
        return jsonify({"msg": "Create task successfully."}), 200

@comment.route("/delete", methods=['POST'])
@jwt_required
def delete():
    if request.get_json():
        current_user = User.query.filter_by(email=get_jwt_identity()).first()
        if not current_user.is_valid:
            return jsonify({"msg": "Your Account isn't invalid"}), 400
        comment_id = request.get_json()["comment_id"]
        if not comment_id:
            return jsonify({"msg": "Missing comment_id parameter"}), 400
        comment = Comment.query.filter_by(id=comment_id).first()
        if not current_user.id == comment.user_id:
            return jsonify({"msg": "you don't have the authority."}), 400
        db.session.delete(comment)
        db.session.commit()
        return jsonify({"msg": "Delete task successfully."}), 200