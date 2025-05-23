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

    from .appmodules.transactions.transactionsRoutes import transactions_bp
    app.register_blueprint(transactions_bp)

    from .appmodules.auditTrail.audittrailRoutes import audit_trail_bp
    app.register_blueprint(audit_trail_bp)



    return app


