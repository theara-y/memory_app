from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from config import Config

db = SQLAlchemy()
login = LoginManager()
bcrypt = Bcrypt()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login.init_app(app)
    bcrypt.init_app(app)

    from .api import memories
    app.register_blueprint(memories.bp)

    from src.main import index
    app.register_blueprint(index.bp)

    from src.auth.routes import bp as auth_routes
    app.register_blueprint(auth_routes)

    from src.main import memory_app
    app.register_blueprint(memory_app.bp)

    return app