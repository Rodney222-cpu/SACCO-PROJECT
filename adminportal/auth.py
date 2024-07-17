from flask import (
    Blueprint,render_template,session,redirect,request
)

from flask_babel import _
from flask_babel import Babel
from .repositories.MessagesRepo import getMessages
from .repositories.UserRepo import UserRepo
import logging
from flask import current_app
auth_bp = Blueprint('auth', __name__)

#logger = logging.getLogger(__name__)

@auth_bp.route('/', methods=('GET', 'POST'))
@auth_bp.route('/login', methods=('GET', 'POST'))
def index():
    current_app.logger.info(msg=session)
    if 'username' in session:
        return redirect('/applayout')
    
    return render_template('auth/login.html', messages=getMessages(app=auth_bp))


@auth_bp.route('/authenticate', methods=('GET', 'POST'))
def authenticate():
    messages=getMessages(app=auth_bp)
    current_app.logger.debug(current_app.config)
    username = request.form.get("username")
    password = request.form.get("password")
    if username is None:
        return {
            "status": "ERROR",
            "message":_("%(msg)s ", msg=messages['invalid_username'] %'Username %s' %(username))
        }
    
    if password is None:
        return {
            "status": "ERROR",
            "message":_("%(msg)s ", msg=messages['invalid_password'])
        } 
    
    if len(username) < 1:
        return {
            "status": "ERROR",
            "message":_("%(msg)s ", msg=messages['invalid_username'] %'Username %s' %(username))
        } 
    
    if len(password) < 1:
        return {
            "status": "ERROR",
            "message":_("%(msg)s ", msg=messages['pass_auth_failed'])
        } 
    
    
    userRepo = UserRepo(current_app)
    auth = userRepo.authenticate_user(username, password)
    if auth['status'] == "OK":
        session['username'] = username
        session['user'] = userRepo.getUserByName(username)
    return auth


@auth_bp.route('/logout', methods=('GET', 'POST'))
def logout():
    session.clear()
    return {"status": "OK","message":_("Log Out was successful")}

