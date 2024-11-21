from flask_babel import _
from flask import (session,request,redirect, render_template)
from flask import current_app
import json
import hashlib
from ...repositories.MessagesRepo import getMessages
from ...repositories.UserRepo import UserRepo
from ...repositories.AuditTrailRepo import AuditTrailRepo
from ...appmodules.auth.ControllerAuth import ControllerAuth

class ControllerUser():
    app=None
    db=None
    messages=None
    def __init__(self, app):
        self.app = app
        self.db = app.db
        self.messages = getMessages(app)
        self.authenticate =ControllerAuth(app)

    def index(self):
        messages=getMessages(app=self.app)
        if 'username' not in session:
            return {
                "status_code" : "001",
                "status": "ERROR",
                "message":_("%(msg)s ", msg=messages['invalid_username'])
            }

        return {
            "status_code":"000",
            "status":"OK",
            "html":render_template('user/user_table.html', messages=getMessages(app=self.app)),
            "js":render_template('user/user.js', messages=getMessages(app=self.app)),    
        }
    
    def getUser_acgsForCombobox(self):
        return [
            {"id":self.messages['view_users'],"text":self.messages['view_users']},
            {"id":self.messages['create_acgs'],"text":self.messages['create_acgs']},
            {"id":self.messages['update_acgs'],"text":self.messages['update_acgs']},
            {"id":self.messages['view_saccos'],"text":self.messages['view_saccos']},
            {"id":self.messages['delete_saccos'],"text":self.messages['delete_saccos']},
            {"id":self.messages['update_saccos'],"text":self.messages['update_saccos']},
            {"id":self.messages['create_saccos'],"text":self.messages['create_saccos']},
            {"id":self.messages['view_users'],"text":self.messages['view_users']},
            {"id":self.messages['delete_users'],"text":self.messages['delete_users']},
            {"id":self.messages['update_users'],"text":self.messages['update_users']},
            {"id":self.messages['create_users'],"text":self.messages['create_users']},
        ]
    
    def addUser(self):
        name = request.form.get("name")
        phone = request.form["phone"]
        email = request.form["email"]
        user_acgs = set(request.form.getlist("user_acgs[]"))
        password = request.form["password"]
        action = "Created a new USER with name: "+name
        data = ""


        if not isinstance(password, str) or not password.strip():
            return {'status':"ERROR", "message":"Password must be a non empty string"}
        
        hashlib.sha256(password.encode()).hexdigest()

        userRepo = UserRepo(current_app)
        user = userRepo.getOneUserByEmail(name)

        auditTrail = AuditTrailRepo(current_app)
        atEntry = auditTrail.addAuditTrail(session['user']['name'], session['user']['email'], action, data)

        if atEntry['status'] != "OK":
            return atEntry


        if user != None :
            return {
                'status':"ERROR", 
                "message":self.messages['error_user_already_exists']
            }
        
        return userRepo.addUser(name,phone,email,password, user_acgs)

    def updateUser(self):
        user_id = request.form.get("id")
        name = request.form.get("name")
        phone = request.form.get("phone")
        email = request.form.get("email")
        user_acgs = set(request.form.getlist("user_acgs[]"))

        userRepo = UserRepo(current_app)

        '''
        Let's first get the existing data before the update
        '''
        userBeforeUpdate = userRepo.getOneUserById(user_id)
        if userBeforeUpdate == None:
            return {
                'status':"ERROR", 
                "message":self.messages['resource_does_not_exist'] %'USER'+name
            }

        user = userRepo.getUserById(user_id)

        if user == None:
            return {
                'status':"ERROR", 
                "message":self.messages['error_user_not_exist']
            }

       
        userSameEmail = userRepo.userWithEmailAndNotId(email, user_id)
        if userSameEmail != None:
            return {
                'status':"ERROR", 
                "message":self.messages['error_user_same_email_exist'].format(userSameEmail["email"])
            }
        
        userBeforeUpdate['created_on'] = userBeforeUpdate['created_on'].strftime("%Y-%m-%d %H:%M:%S")
        userBeforeUpdate['updated_on'] = userBeforeUpdate['updated_on'].strftime("%Y-%m-%d %H:%M:%S")
        oldData = json.dumps(userBeforeUpdate)
        action = "Updated user "+userBeforeUpdate['name']+" to "+name

    
        return userRepo.updateUser(user_id, name, phone,  email,  user_acgs, session['user'], action, oldData)
    
    def getUser(self):

        userRepo = UserRepo(current_app)
        user = userRepo.getUser()

        return {
            "total": len(user),
            "rows": user
        }
        
    def deleteUser(self):
        rows = request.get_json()

        userRepo = UserRepo(current_app)
        '''
        Let's first get the existing data before the delete
        '''
        for user in rows:
            userBeforeDelete = userRepo.getOneUserById(user['id'])
            if userBeforeDelete == None:
                return {
                    'status':"ERROR",
                    "message":self.messages['resource_does_not_exist']%'USER'
                }
            
            userBeforeDelete['created_on']=userBeforeDelete['created_on'].strftime("%Y-%m-%d %H:%M:%S")
            userBeforeDelete['updated_on']=userBeforeDelete['updated_on'].strftime("%Y-%m-%d %H:%M:%S")
            oldData = json.dumps(userBeforeDelete)
            action = "Deleted user"+userBeforeDelete['name']+""

        return userRepo.deleteUser(rows, session['user'], oldData, action)
            