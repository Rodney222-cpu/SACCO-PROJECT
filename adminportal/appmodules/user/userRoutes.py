from flask import (
    Blueprint,render_template,session,redirect,request
)

from flask_babel import _
from flask_babel import Babel
from ...repositories.MessagesRepo import getMessages
from ...repositories.UserRepo import UserRepo
import logging
from flask import current_app
from .ControllerUser import ControllerUser
user_bp = Blueprint('user', __name__)

#logger = logging.getLogger(__name__)

@user_bp.route('/user', methods=('GET', 'POST'))
def index():
    controllerUser = ControllerUser(current_app)
    return controllerUser.index()

@user_bp.route('/userGetUser_acgsForCombo', methods=('GET', 'POST'))
def userGetUser_acgsForCombo():
    controllerUser = ControllerUser(current_app)
    return controllerUser.getUser_acgsForCombobox()


@user_bp.route('/addUser', methods=('GET', 'POST'))
def addUser():
    controllerUser = ControllerUser(current_app)
    return controllerUser.addUser()

@user_bp.route('/updateUser', methods=('GET', 'POST'))
def updateUser():
    controllerUser = ControllerUser(current_app)
    return controllerUser.updateUser()

@user_bp.route('/getUser', methods=('GET', 'POST'))
def getUser():
    controllerUser = ControllerUser(current_app)
    return controllerUser.getUser()

@user_bp.route('/deleteUser', methods=('GET', 'POST'))
def deleteUser():
    controllerUser = ControllerUser(current_app)
    return controllerUser.deleteUser()   



 




    