from flask import (
    Blueprint,render_template,session,redirect,request
)

from flask_babel import _
from flask_babel import Babel
from ...repositories.MessagesRepo import getMessages
from ...repositories.UserRepo import UserRepo
import logging
from flask import current_app
auth_bp = Blueprint('auth', __name__)
from .ControllerAuth import ControllerAuth

@auth_bp.route('/', methods=('GET', 'POST'))
@auth_bp.route('/login', methods=('GET', 'POST'))
def index():
    authController = ControllerAuth(current_app)
    return authController.index()


@auth_bp.route('/authenticate', methods=('GET', 'POST'))
def authenticate():
    authController = ControllerAuth(current_app)
    return authController.authenticate()


@auth_bp.route('/logout', methods=('GET', 'POST'))
def logout():
    authController = ControllerAuth(current_app)
    return authController.logout()
