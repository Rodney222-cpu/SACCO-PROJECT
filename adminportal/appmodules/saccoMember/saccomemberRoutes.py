from flask import (
    Blueprint,render_template,session,redirect,request
)

from flask_babel import _
from flask_babel import Babel
from ...repositories.MessagesRepo import getMessages
from ...repositories.SaccoMemberRepo import SaccoMemberRepo
import logging
from flask import current_app
from .ControllerSaccoMember import ControllerSaccoMember
sacco_member_bp = Blueprint('saccomember', __name__)

#logger = logging.getLogger(_name_)

@sacco_member_bp.route('/saccomember', methods=('GET', 'POST'))
def index():
    controllerSaccomember = ControllerSaccoMember(current_app)
    return controllerSaccomember.index()

@sacco_member_bp.route('/addSaccoMember', methods=('GET', 'POST'))
def addSaccoMember():
    controllerSaccomember = ControllerSaccoMember(current_app)
    return controllerSaccomember.addSaccoMember()


@sacco_member_bp.route('/getSaccoMember', methods=('GET', 'POST'))
def getSaccoMember():
    controllerSaccomember = ControllerSaccoMember(current_app)
    return controllerSaccomember.getSaccoMembers()

@sacco_member_bp.route('/deleteSaccoMembers', methods=('GET', 'POST'))
def deleteSaccoMembers():
    controllerSaccomember = ControllerSaccoMember(current_app)
    return controllerSaccomember.deleteSaccoMembers()

@sacco_member_bp.route('/updateSaccoMember', methods=('GET', 'POST'))
def updateSaccoMember():
    controllerSaccoMember = ControllerSaccoMember(current_app)
    return controllerSaccoMember.updateSaccoMember()



