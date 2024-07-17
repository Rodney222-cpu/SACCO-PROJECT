from flask import (
    Blueprint,render_template,session,redirect,request
)

from flask_babel import _
from flask_babel import Babel
from .repositories.MessagesRepo import getMessages
from .repositories.UserRepo import UserRepo
import logging
from flask import current_app
acg_bp = Blueprint('acg', __name__)

#logger = logging.getLogger(__name__)

@acg_bp.route('/acgs', methods=('GET', 'POST'))
def acgs():
    messages=getMessages(app=acg_bp)
    if 'username' not in session:
        return {
            "status_code" : "001",
            "status": "ERROR",
            "message":_("%(msg)s ", msg=messages['invalid_username'])
        }

    return render_template('acgs/acgs_table.html', messages=getMessages(app=acg_bp))
    

