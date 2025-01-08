from flask_babel import _
from flask import (session,request,redirect, render_template)
from flask import current_app
import hashlib
from ...repositories.MessagesRepo import getMessages
from ...repositories.SaccoMemberRepo import SaccoMemberRepo
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
        if 'email' in session:
            return redirect('/applayout')
        
        return render_template('auth/login.html', messages=self.messages)

    def authenticate(self):
        current_app.logger.debug(current_app.config)
        sacco_id = request.form.get("sacco_id")
        phone_or_email = request.form.get("phone_or_email")
        password = request.form.get("password")
        if sacco_id is None:
            return {
                "status": "ERROR",
                "message":_("%(msg)s ", msg=self.messages['invalid_saccoid'] %'Sacco id %s' %(sacco_id))
            }
        
        if password is None:
            return {
                "status": "ERROR",
                "message":_("%(msg)s ", msg=self.messages['invalid_password'])
            } 
        
        if phone_or_email is None:
            return {
                "status": "ERROR",
                "message":_("%(msg)s", msg=self.messages['invalid_phone_or_email'])
            }
        
        if len(sacco_id) < 1:
            return {
                "status": "ERROR",
                "message":_("%(msg)s ", msg=self.messages['invalid_saccoid'] %'Sacco id %s' %(sacco_id))
            } 
        
        if len(phone_or_email) < 1:
            return {
                "status": "ERROR",
                "message":_("%(msg)s", msg=self.messages['invalid_phone_or_email'] %'Phone %s' %(phone_or_email))
            }
        
        if len(password) < 1:
            return {
                "status": "ERROR",
                "message":_("%(msg)s ", msg=self.messages['pass_auth_failed'])
            } 
        
        
        saccomemberRepo = SaccoMemberRepo(current_app)
        saccomember = saccomemberRepo.getOneSaccoMemberBySaccoId(sacco_id)
        print(saccomember, file=sys.stderr)
        if not saccomember:
            return {'status':"ERROR", "message":_('%(msg)s', msg=self.messages['error_sacco_member_not_exist'])}
        else:
            #Check user's password
            hashed_pw = hashlib.sha256(password.encode()).hexdigest()
            if saccomember['password'] == hashed_pw:
                session['sacco_id'] = sacco_id
                session['phone_or_email'] = phone_or_email
                session['saccomember'] = saccomemberRepo.getOneSaccoMemberBySaccoId()
                
                return {'status':"OK", "message":_('%(msg)s', msg=self.messages['sacco_member_authenticated'])}
           
            else:
                return {'status':"ERROR", "message":_('%(msg)s', msg=self.messages['pass_auth_failed'])}

            

    def logout(self):        
        session.clear()
        return {"status": "OK","message":_("Log Out was successful")}