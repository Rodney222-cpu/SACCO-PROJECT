from flask import Flask
from flask_babel import Babel
from flask_mysqldb import MySQL

def create_app():
    app = Flask(__name__)


    #app.config.from_object('frontendportal.default_settings')
    app.config.from_envvar('FRONTENDPORTAL_SETTINGS')

    app.db = MySQL(app)

    babel = Babel(app)

    #Register Blueprints here
    from .appmodules.auth.authRoots import auth_bp
    app.register_blueprint(auth_bp)

    from .appmodules.applayout.applayoutRootes import applayout_bp
    app.register_blueprint(applayout_bp)

    from .appmodules.members.membersRoutes import members_bp
    app.register_blueprint(members_bp)



    return app


