from flask import(
    Blueprint,render_template,session,redirect,request
)

from flask_babel import _
from flask_babel import Babel
from ...repositories.MessagesRepo import getMessages
from ...repositories.SaccoMemberRepo import SaccoMemberRepo
import logging
from flask import current_app
from .ControllerMembers import ControllerMembers
members_bp = Blueprint('members', __name__)

#logger = logging.getLogger(_name_)

@members_bp.route('/members', methods=('GET', 'POST'))
def index():
    controllerMembers = ControllerMembers(current_app)
    return controllerMembers.index()

@members_bp.route('/getMember', methods=('GET', 'POST'))
def getMember():
    controllerMembers = ControllerMembers(current_app)
    return controllerMembers.getMembers()

@members_bp.route('/addMember', methods=('GET', 'POST'))
def addMember():
    controllerMembers = ControllerMembers(current_app)
    return controllerMembers.addMember()

@members_bp.route('/deleteMembers', methods=('GET', 'POST'))
def deleteMembers():
    controllerMembers = ControllerMembers(current_app)
    return controllerMembers.deleteMembers()

@members_bp.route('/updateMember', methods=('GET', 'POST'))
def updateMember():
    controllerMembers = ControllerMembers(current_app)
    return controllerMembers.updateMember()
