from flask import (
    Blueprint,render_template,session,redirect,request
)

from flask_babel import _
from flask_babel import Babel
from ...repositories.MessagesRepo import getMessages
from ...repositories.SaccoRepo import SaccoRepo
import logging
from flask import current_app
from .ControllerSacco import ControllerSacco
sacco_bp = Blueprint('sacco', __name__)

#logger = logging.getLogger(__name__)

@sacco_bp.route('/sacco', methods=('GET', 'POST'))
def index():
    controllerSacco = ControllerSacco(current_app)
    return controllerSacco.index()

@sacco_bp.route('/addSacco', methods=('GET', 'POST'))
def addSacco():
    controllerSacco = ControllerSacco(current_app)
    return controllerSacco.addSacco()


@sacco_bp.route('/getSacco', methods=('GET', 'POST'))
def getSacco():
    controllerSacco = ControllerSacco(current_app)
    return controllerSacco.getSacco()

@sacco_bp.route('/deleteSacco', methods=('GET', 'POST'))
def deleteSacco():
    controllerSacco = ControllerSacco(current_app)
    return controllerSacco.deleteSacco()   

@sacco_bp.route('/updateSacco', methods=('GET', 'POST'))
def updateSacco():
    controllerSacco = ControllerSacco(current_app)
    return controllerSacco.updateSacco()
 




    