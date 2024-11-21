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
    from .appmodules.auth.authRoots import auth_bp
    app.register_blueprint(auth_bp)

    from .appmodules.applayout.applayoutRootes import applayout_bp
    app.register_blueprint(applayout_bp)

    from .appmodules.acg.acgRoutes import acg_bp
    app.register_blueprint(acg_bp)

    from .appmodules.user.userRoutes import user_bp
    app.register_blueprint(user_bp)

    from .appmodules.sacco.saccoRoutes import sacco_bp
    app.register_blueprint(sacco_bp)

    from .appmodules.saccoMember.saccomemberRoutes import sacco_member_bp
    app.register_blueprint(sacco_member_bp)

    from .appmodules.auditTrail.audittrailRoutes import audit_trail_bp
    app.register_blueprint(audit_trail_bp)

    from .appmodules.transactions.transactionsRoutes import transactions_bp
    app.register_blueprint(transactions_bp)




    

    
    return app

