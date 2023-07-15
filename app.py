from os import environ
from flask import Flask
from init import db, ma, bcrypt, jwt
from blueprints.cli_bp import db_commands
from blueprints.tasks_bp import tasks_bp
from blueprints.auth_bp import auth_bp


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = environ.get('DB_URI')
    app.config["JWT_SECRET_KEY"] = environ.get('JWT_SECRET')

    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(db_commands)
    app.register_blueprint(tasks_bp)
    app.register_blueprint(auth_bp)


    return app