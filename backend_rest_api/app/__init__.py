from flask import Flask, jsonify
from flask_mongoengine import MongoEngine
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from werkzeug.exceptions import HTTPException

from app.config import Config
from app.routes import add_resources
from app.scheduler import add_scheduler
from app.error_handlers import setup_error_handlers


def create_app() -> Flask:
    app = Flask(__name__)

    app.config['MONGODB_SETTINGS'] = {'db': 'alkymi'}
    app.config['JWT_SECRET_KEY'] = Config.AUTH.JWT_SECRET_KEY
    app.config['PROPAGATE_EXCEPTIONS'] = True  # This flag is needed to prevent Gunicorn from overriding Flask-Restful's response messages

    setup_error_handlers(app)
    db = MongoEngine(app)
    add_resources(app)
    bcrypt = Bcrypt(app)
    jwt = JWTManager(app)
    add_scheduler(app)
    return app
