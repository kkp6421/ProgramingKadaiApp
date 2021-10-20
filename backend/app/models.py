from app import db
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    is_valid = db.Column(db.Boolean, default=False)
    
    given_activation_token = db.Column(db.String(128), default=None)
    given_activation_token_date = db.Column(db.DateTime, default=None)
    given_reset_password_token = db.Column(db.String(128), default=None)
    given_reset_password_token_date = db.Column(db.DateTime, default=None)
    
    comments = db.relationship('Comment', backref='comment')
    posts = db.relationship("Post", backref="post")


    @property
    def password(self):
        raise AttributeError('password is not a readable attributes.')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "<User: {id: %r, username: %r, email: %r, password_hash: %r, posts_count: %r, comments_count: %r}>" \
               % (self.id, self.username, self.email, self.password_hash, len(self.posts), len(self.comments))
            
class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(512), nullable=False)
    post_date = db.Column(db.DateTime, default=datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comments = db.relationship("Comment", backref="post_comment")

    def __repr__(self):
        return "<Post: {id: %r, text: %r, post_date: %r, user_id: %r, comments_count: %r}>" \
                % (self.id, self.text, self.post_date, self.user_id, len(self.comments))

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(512), nullable=False)
    comment_date = db.Column(db.DateTime, default=datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    
    def __repr__(self):
        return "<Task: {id: %r, text: %r, comment_date: %r, user_id: %r, post_id: %r}>" \
               % (self.id, self.text, self.comment_date, self.user_id, self.post_id)