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

#logger = logging.getLogger(__name__)

@acg_bp.route('/acgs', methods=('GET', 'POST'))
def index():
    controllerAcg = ControllerAcg(current_app)
    return controllerAcg.index()
    

