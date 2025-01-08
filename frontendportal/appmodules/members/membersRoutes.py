from flask import(
    Blueprint,render_template,session,redirect,request
)

from flask_babel import _
from flask_babel import Babel
from ...repositories.MessagesRepo import getMessages
from ...repositories.MembersRepo import MembersRepo
import logging
from flask import current_app
from .ControllerMembers import ControllerMembers
members_bp = Blueprint('members', __name__)

#logger = logging.getLogger(_name_)

@members_bp.route('/members', methods=('GET', 'POST'))
def index():
    controllerMembers = ControllerMembers(current_app)
    return controllerMembers.index()