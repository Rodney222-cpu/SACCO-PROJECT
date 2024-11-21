from flask_babel import _
from flask import (session,request, redirect, render_template)
from flask import current_app
import json
from ...repositories.MessagesRepo import getMessages
from ...repositories.SaccoMemberRepo import SaccoMemberRepo
from ...repositories.SaccoRepo import SaccoRepo
from ...repositories.AuditTrailRepo import AuditTrailRepo
from ...appmodules.auth.ControllerAuth import ControllerAuth


class ControllerSaccoMember():
    app=None
    db=None
    messages=None
    def __init__(self, app):
        self.app = app
        self.db = app.db
        self.messages = getMessages(app)
        self.authenticate =ControllerAuth(app)

    def index(self):
        sacco_id = request.args.get("sacco_id")
        messages=getMessages(app=self.app)
        saccoRepo = SaccoRepo(current_app)
        sacco = saccoRepo.getSaccoById(sacco_id)
        if 'username' not in session:
            return {
                "status_code" : "001",
                "status": "ERROR",
                "message":_("%(msg)s ", msg=messages['invalid_username'])
            }

        return {
            "status_code":"000",
            "status":"OK",
            "html":render_template('saccomember/sacco_member_table.html', messages=getMessages(app=self.app), sacco_id=sacco_id, sacco=sacco),
            "js":render_template('saccomember/saccomember.js', messages=getMessages(app=self.app), sacco_id=sacco_id, sacco=sacco),    
        }
        
    
    def addSaccoMember(self):
        sacco_id = request.form.get('sacco_id')
        account_number = request.form["account_number"]
        fname = request.form["fname"]
        lname = request.form["lname"]
        gender = request.form["gender"]
        phone = request.form["phone"]
        email = request.form["email"]
        role = request.form["role"]
        balance = request.form["balance"]
        next_of_kin_name = request.form["next_of_kin_name"]
        date_of_birth = request.form["date_of_birth"]
        action = "Created a new SACCO MEMBER with"+email
        data =""

        saccomemberRepo = SaccoMemberRepo(current_app)
        saccomember = saccomemberRepo.getOneSaccoMemberByEmail(email)

        auditTrail = AuditTrailRepo(current_app)
        atEntry = auditTrail.addAuditTrail(session['user']['name'], session['user']['email'], action, data)

        if atEntry['status'] != "OK":
            return atEntry
        



        if saccomember != None :
            return {
                'status':"ERROR", 
                "message":self.messages['error_sacco_member_already_exists']
            }
        
        return saccomemberRepo.addSaccoMember(
            sacco_id,
            account_number, 
            fname, 
            lname, 
            gender, 
            phone, 
            email, 
            role, 
            balance, 
            next_of_kin_name, 
            date_of_birth
            )

   
    
    def getSaccoMembers(self):
        sacco_id = request.args.get("sacco_id")
        saccomemberRepo = SaccoMemberRepo(current_app)
        saccomembers = saccomemberRepo.getSaccoMembers(sacco_id)

        return {
            "total": len(saccomembers),
            "rows": saccomembers
        }
    
    def deleteSaccoMembers(self):
        rows = request.get_json()

        saccomemberRepo = SaccoMemberRepo(current_app)

        '''
        Let's first get the existing data before the delete
        '''
        for saccomember in rows:

            saccomemberBeforeDelete=saccomemberRepo.getOneSaccoMemberById(saccomember['id'])
            if saccomemberRepo == None:
                return {
                    'status':"ERROR",
                    "message":self.messages["resource_does_not_exist"]%'SACCOMEMBER'
                }
            
            saccomemberBeforeDelete['date_of_birth']=saccomemberBeforeDelete['date_of_birth'].strftime("%Y-%m-%d %H:%M:%S")
            saccomemberBeforeDelete['created_on']=saccomemberBeforeDelete['created_on'].strftime("%Y-%m-%d %H:%M:%S")
            saccomemberBeforeDelete['updated_on']=saccomemberBeforeDelete['updated_on'].strftime("%Y-%m-%d %H:%M:%S")
            oldData=json.dumps(saccomemberBeforeDelete)
            action="Deleted sacco member"+saccomemberBeforeDelete['email']+" "

        return saccomemberRepo.deleteSaccoMembers(rows, session['user'], action, oldData)
    

    def updateSaccoMember(self):
        id = request.form.get("id")
        sacco_id = request.form.get("sacco_id")
        account_number = request.form.get("account_number")
        fname = request.form.get("fname")
        lname = request.form.get("lname")
        gender = request.form.get("gender")
        phone = request.form.get("phone")
        email = request.form.get("email")
        role = request.form.get("role")
        balance = request.form.get("balance")
        next_of_kin_name = request.form.get("next_of_kin_name")
        date_of_birth = request.form.get("date_of_birth")

        
        saccomemberRepo = SaccoMemberRepo(current_app)

        '''
        Let's first get the existing data before the update
        '''
        saccomemberBeforeUpdate = saccomemberRepo.getOneSaccoMemberById(id)
        if saccomemberBeforeUpdate == None:
            return {
                'status':"ERROR", 
                "message":self.messages['resource_does_not_exist'] %'SACCO MEMBER'+email
            }

        saccomember = saccomemberRepo.getSaccoMemberById(id)

        if saccomember == None:
            return {
                'status':"ERROR", 
                "message":self.messages['error_sacco_member_not_exist']
            }

       
        saccomemberSameEmail = saccomemberRepo.saccomemberEmailAndNotId(email, id)
        if saccomemberSameEmail!= None:
            return {
                'status':"ERROR", 
                "message":self.messages['error_sacco_member_same_email_exist'].format(saccomemberSameEmail["email"])
            }
        
        saccomemberBeforeUpdate['date_of_birth'] = saccomemberBeforeUpdate['date_of_birth'].strftime("%Y-%m-%d %H:%M:%S")
        saccomemberBeforeUpdate['created_on'] = saccomemberBeforeUpdate['created_on'].strftime("%Y-%m-%d %H:%M:%S")
        saccomemberBeforeUpdate['updated_on'] = saccomemberBeforeUpdate['updated_on'].strftime("%Y-%m-%d %H:%M:%S")
        oldData = json.dumps(saccomemberBeforeUpdate)
        action = "Updated sacco member "+saccomemberBeforeUpdate['email']+" to "+email

            
        return saccomemberRepo.updateSaccoMember(id, sacco_id, account_number, fname, lname, gender, phone, email, role, balance, next_of_kin_name, date_of_birth, session['user'], action, oldData)



            