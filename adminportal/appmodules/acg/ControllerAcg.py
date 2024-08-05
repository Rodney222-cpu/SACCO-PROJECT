from flask_babel import _
from flask import (session,request,redirect, render_template)
from flask import current_app
import hashlib
from ...repositories.MessagesRepo import getMessages
from ...repositories.AcgRepo import AcgRepo

class ControllerAcg():
    app=None
    db=None
    messages=None
    def __init__(self, app):
        self.app = app
        self.db = app.db
        self.messages = getMessages(app)

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
            "html":render_template('acgs/acgs_table.html', messages=getMessages(app=self.app)),
            "js":render_template('acgs/acgs.js', messages=getMessages(app=self.app)),    
        }
    
    def getPrivilegesForCombobox(self):
        return [
            {"id":self.messages['view_users'],"text":self.messages['view_users']},
            {"id":self.messages['create_users'],"text":self.messages['create_users']},
            {"id":self.messages['update_users'],"text":self.messages['update_users']},
            {"id":self.messages['view_saccos'],"text":self.messages['view_saccos']},
            {"id":self.messages['delete_saccos'],"text":self.messages['delete_saccos']},
            {"id":self.messages['update_saccos'],"text":self.messages['update_saccos']},
            {"id":self.messages['create_saccos'],"text":self.messages['create_saccos']},
            {"id":self.messages['view_acgs'],"text":self.messages['view_acgs']},
            {"id":self.messages['delete_acgs'],"text":self.messages['delete_acgs']},
            {"id":self.messages['update_acgs'],"text":self.messages['update_acgs']},
            {"id":self.messages['create_acgs'],"text":self.messages['create_acgs']},
        ]
    
    def addAcg(self):
        name = request.form.get("name")
        privileges = request.form.getlist("privilage_name[]")

        acgRepo = AcgRepo(current_app)
        acg = acgRepo.getOneAcgByName(name)

        if acg != None :
            return {
                'status':"OK", 
                "message":self.messages['error_acg_already_exists']
            }
        
        unique_privileges = set()
        dupes = []

        for x in privileges:
            if x in unique_privileges:
                dupes.append(x)
            else:
                unique_privileges.add(x)

        return acgRepo.addAcg(name, unique_privileges)
            