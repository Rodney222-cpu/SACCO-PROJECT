from flask_babel import _
from flask import (session,request,redirect, render_template)
from flask import current_app
import hashlib
from ...repositories.MessagesRepo import getMessages
from ...repositories.UserRepo import UserRepo 
from ...repositories.AuditTrailRepo import AuditTrailRepo
import sys

class ControllerAuth():
    app=None
    db=None
    messages=None
    def __init__(self, app):
        self.app = app
        self.db = app.db
        self.messages = getMessages(app)

    def index(self):
        current_app.logger.info(msg=session)
        if 'username' in session:
            return redirect('/applayout')
        
        return render_template('auth/login.html', messages=self.messages)

    def authenticate(self):
        current_app.logger.debug(current_app.config)
        username = request.form.get("username")
        password = request.form.get("password")
        if username is None:
            return {
                "status": "ERROR",
                "message":_("%(msg)s ", msg=self.messages['invalid_username'] %'Username %s' %(username))
            }
        
        if password is None:
            return {
                "status": "ERROR",
                "message":_("%(msg)s ", msg=self.messages['invalid_password'])
            } 
        
        if len(username) < 1:
            return {
                "status": "ERROR",
                "message":_("%(msg)s ", msg=self.messages['invalid_username'] %'Username %s' %(username))
            } 
        
        if len(password) < 1:
            return {
                "status": "ERROR",
                "message":_("%(msg)s ", msg=self.messages['pass_auth_failed'])
            } 
        
        
        userRepo = UserRepo(current_app)
        auditTrail = AuditTrailRepo(current_app)
        user = userRepo.getUserByUsername(username)
        print(user, file=sys.stderr)
        if not user:
            return {'status':"ERROR", "message":_('%(msg)s', msg=self.messages['error_user_not_exist'])}
        else:
            #Check user's password
            hashed_pw = hashlib.sha256(password.encode()).hexdigest()
            if user['password'] == hashed_pw:
                session['username'] = username
                session['user'] = userRepo.getUserByUsername(username)
                userAgent = request.user_agent.string
                userIp = request.remote_addr
                action = "Logged in from "+userIp+", UserAgent: "+userAgent
                atEntry = auditTrail.addAuditTrail(user['name'], user['email'], action, "")
                if atEntry['status'] != "OK":
                    return atEntry
                
                return {'status':"OK", "message":_('%(msg)s', msg=self.messages['user_authenticated'])}
           
            else:
                return {'status':"ERROR", "message":_('%(msg)s', msg=self.messages['pass_auth_failed'])}
            

    def logout(self):
        auditTrail = AuditTrailRepo(current_app)
        action = "Logged Out"
        atEntry = auditTrail.addAuditTrail(session['user']['name'], session['user']['email'], action, "")
        if atEntry['status'] != "OK":
            return atEntry
        
        session.clear()
        return {"status": "OK","message":_("Log Out was successful")}