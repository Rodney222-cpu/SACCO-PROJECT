from flask import Flask
from flask_babel import Babel
from flask_mysqldb import MySQL

def create_app():
    app = Flask(__name__)

    #app.config.from_object('adminportal.default_settings')
    app.config.from_envvar('ADMINPORTAL_SETTINGS')

    app.db = MySQL(app)

    babel = Babel(app)

    # Register blueprints here
    from .auth import auth_bp
    app.register_blueprint(auth_bp)

    from .applayout import applayout_bp
    app.register_blueprint(applayout_bp)

    from .acg import acg_bp
    app.register_blueprint(acg_bp)
    
    return app

