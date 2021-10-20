from flask import Flask
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_mail import Mail
from config import config


moment = Moment()
db = SQLAlchemy()
jwt = JWTManager()
cors = CORS()
mail = Mail()

def create_app(config_name):

    app = Flask(__name__, template_folder="../../frontend/dist", static_folder="../../frontend/dist/static")
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    moment.init_app(app)
    db.init_app(app)
    jwt.init_app(app)
    cors.init_app(app)
    mail.init_app(app)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .comment import comment as comment_blueprint
    app.register_blueprint(comment_blueprint, url_prefix='/api/comments')

    from .post import post as post_blueprint
    app.register_blueprint(post_blueprint, url_prefix='/api/posts')

    from .user import user as user_blueprint
    app.register_blueprint(user_blueprint, url_prefix='/api/users')

    return app