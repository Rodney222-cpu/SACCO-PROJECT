from flask_babel import _
from flask import (session,request,redirect, render_template)
from flask import current_app
import json
from ...repositories.MessagesRepo import getMessages
from ...repositories.SaccoRepo import SaccoRepo
from ...repositories.AuditTrailRepo import AuditTrailRepo
from ...appmodules.auth.ControllerAuth import ControllerAuth

class ControllerSacco():
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
            "html":render_template('sacco/sacco_table.html', messages=getMessages(app=self.app)),
            "js":render_template('sacco/sacco.js', messages=getMessages(app=self.app)),    
        }
    
      
    def addSacco(self):
        group_id = request.form["group_id"]
        name = request.form["name"]
        location = request.form["location"]
        action = "Created a new SACCO with name: "+name
        data = ""
       
    
        saccoRepo = SaccoRepo(current_app)
        sacco = saccoRepo.getOneSaccoByGroupId(name)

        auditTrail = AuditTrailRepo(current_app)
        atEntry = auditTrail.addAuditTrail(session['user']['name'], session['user']['email'], action, data)

        if atEntry['status'] != "OK":
            return atEntry
        

        if sacco != None :
            return {
                'status':"ERROR", 
                "message":self.messages['error_sacco_already_exists']
            }
        
        return saccoRepo.addSacco(group_id, name, location)

       
    def getSacco(self):

        saccoRepo = SaccoRepo(current_app)
        sacco = saccoRepo.getSacco()

        return {
            "total": len(sacco),
            "rows": sacco
        }
    
    def deleteSacco(self):
        rows = request.get_json()

        saccoRepo = SaccoRepo(current_app)
        
        '''
        Let's first get the existing data before the delete
        '''
        for sacco in rows:
            saccoBeforeDelete=saccoRepo.getOneSaccoById(sacco['id'])
            if saccoBeforeDelete == None:
                return {
                    'status':"ERROR",
                    "message":self.messages["resource_does_not_exist"]%'SACCO'
                }
            saccoBeforeDelete['created_on']=saccoBeforeDelete['created_on'].strftime("%Y-%m-%d %H:%M:%S")
            saccoBeforeDelete['updated_on']=saccoBeforeDelete['updated_on'].strftime("%Y-%m-%d %H:%M:%S")
            oldData=json.dumps(saccoBeforeDelete)
            action="Deleted sacco"+saccoBeforeDelete['name']+""

        return saccoRepo.deleteSacco(rows, session['user'], oldData, action)
    

    def updateSacco(self):
        id = request.form.get("id")
        group_id = request.form.get("group_id")
        name = request.form.get("name")
        location = request.form.get("location")
        
        saccoRepo = SaccoRepo(current_app)

        '''
        Let's first get the existing data before the update
        '''
        saccoBeforeUpdate = saccoRepo.getOneSaccoById(id)
        if saccoBeforeUpdate == None:
            return {
                'status':"ERROR", 
                "message":self.messages['resource_does_not_exist'] %'SACCO'+name
            }
        
        sacco = saccoRepo.getSaccoById(id)
        if sacco == None:
            return {
                'status':"ERROR", 
                "message":self.messages['error_sacco_not_exist']
            }

       
        saccoSameGroupId = saccoRepo.saccoWithGroupIdAndNotId(group_id, id)
        if saccoSameGroupId != None:
            return {
                'status':"ERROR", 
                "message":self.messages['error_sacco_same_group_id_exist'].format(saccoSameGroupId["group_id"])
            }
        
        saccoBeforeUpdate['created_on'] = saccoBeforeUpdate['created_on'].strftime("%Y-%m-%d %H:%M:%S")
        saccoBeforeUpdate['updated_on'] = saccoBeforeUpdate['updated_on'].strftime("%Y-%m-%d %H:%M:%S")
        oldData = json.dumps(saccoBeforeUpdate)
        action = "Updated sacco "+saccoBeforeUpdate['name']+" to "+name
    
    
        return saccoRepo.updateSacco(id, group_id, name, location, session['user'], action, oldData)

            