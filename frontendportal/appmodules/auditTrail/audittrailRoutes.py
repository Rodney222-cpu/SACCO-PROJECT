from flask import (
    Blueprint,session,render_template,redirect,request
)

from flask_babel import _
from flask_babel import Babel
from ...repositories.MessagesRepo import getMessages
from ...repositories.AuditTrailRepo import AuditTrailRepo
import logging
from flask import current_app
from .ControllerAuditTrail import ControllerAuditTrail
audit_trail_bp = Blueprint('audittrail', __name__)

#logger = logging.getLogger(_name_)

@audit_trail_bp.route('/audittrail', methods=('GET', 'POST'))
def index():
    controllerAudittrail = ControllerAuditTrail(current_app)
    return controllerAudittrail.index()

@audit_trail_bp.route('/getAuditTrail', methods=('GET', 'POST'))
def getAuditTrail():
    controllerAudittrail = ControllerAuditTrail(current_app)
    return controllerAudittrail.getAuditTrails()




