from flask import (
    Blueprint,render_template,session,redirect,request
)

from flask_babel import _
from flask_babel import Babel
from ...repositories.MessagesRepo import getMessages
from ...repositories.UserRepo import UserRepo
import logging
from flask import current_app
from .ControllerAcg import ControllerAcg
acg_bp = Blueprint('acg', __name__)

#logger = logging.getLogger(_name_)

@acg_bp.route('/acgs', methods=('GET', 'POST'))
def index():
    controllerAcg = ControllerAcg(current_app)
    return controllerAcg.index()

@acg_bp.route('/acgsGetPrivilegesForCombo', methods=('GET', 'POST'))
def acgsGetPrivilegesForCombo():
    controllerAcg = ControllerAcg(current_app)
    return controllerAcg.getPrivilegesForCombobox()

@acg_bp.route('/addAcg', methods=('GET', 'POST'))
def addAcg():
    controllerAcg = ControllerAcg(current_app)
    return controllerAcg.addAcg()

@acg_bp.route('/updateAcg', methods=('GET', 'POST'))
def updateAcg():
    controllerAcg = ControllerAcg(current_app)
    return controllerAcg.updateAcg()

@acg_bp.route('/getAcgs', methods=('GET', 'POST'))
def getAcgs():
    controllerAcg = ControllerAcg(current_app)
    return controllerAcg.getAcgs()

@acg_bp.route('/deleteAcgs', methods=('GET', 'POST'))
def deleteAcgs():
    controllerAcg = ControllerAcg(current_app)
    return controllerAcg.deleteAcgs()

@acg_bp.route('/getAcgsForCombo', methods=('GET', 'POST'))
def getAcgsForCombo():
    controllerAcg = ControllerAcg(current_app)
    return controllerAcg.getAcgsForCombo()