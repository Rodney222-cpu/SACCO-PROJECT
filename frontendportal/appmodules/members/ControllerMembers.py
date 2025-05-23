from flask_babel import _
from flask import (session, render_template, redirect, request)
from flask import current_app
import hashlib
import json
from ...repositories.MessagesRepo import getMessages
from ...repositories.SaccoMemberRepo import SaccoMemberRepo
from ...repositories.AuditTrailRepo import AuditTrailRepo
from ...repositories.SaccoRepo import SaccoRepo
from ...appmodules.auth.ControllerAuth import ControllerAuth



class ControllerMembers():
    app=None
    db=None
    messages=None
    def __init__(self, app):
        self.app = app
        self.db = app.db
        self.messages = getMessages(app)
        self.authenticate = ControllerAuth(app)

    def index(self):
        sacco_id = request.args.get("sacco_id")
        messages = getMessages(app=self.app)
        saccoRepo = SaccoRepo(current_app)
        sacco = saccoRepo.getSaccoById(sacco_id)

        if not 'sacco_id' and not 'username' in session:
            return {
                "status_code" : "001",
                "status": "ERROR",
                "message":_("%(msg)s", msg=messages['invalid_sacco_id_and_username'])
            }
        
        return {
            "status_code": "000",
            "status": "OK",
            "html":render_template('members/members_table.html', messages=getMessages(app=self.app), sacco=sacco, sacco_id=sacco_id),
             "js":render_template('members/members.js', messages=getMessages(app=self.app), sacco=sacco, sacco_id=sacco_id)
        }

    def getMembers(self):
        sacco_id = request.args.get("sacco_id")
        membersRepo =  SaccoMemberRepo(current_app)
        members = membersRepo.getSaccoMembers(sacco_id)

        return {
            "total" : len(members),
            "rows" : members
        } 
    

    def addMember(self):
        sacco_id = request.form.get('sacco_id')
        account_number = request.form["account_number"]
        fname = request.form["fname"]
        lname = request.form["lname"]
        gender = request.form["gender"]
        phone = request.form["phone"]
        email = request.form["email"]
        role = request.form["role"]
        next_of_kin_name = request.form["next_of_kin_name"]
        date_of_birth = request.form["date_of_birth"]
        password = request.form["password"]
        action = "Created a new SACCO MEMBER with"+email
        data =""

       
        if not isinstance(password, str) or not password.strip():
            return {'status':"ERROR", "message":"Password must be a non empty string"}
        
        hashlib.sha256(password.encode()).hexdigest()

        saccomemberRepo = SaccoMemberRepo(current_app)
        saccomember = saccomemberRepo.getOneSaccoMemberByEmail(email)

        auditTrail = AuditTrailRepo(current_app)
        atEntry = auditTrail.addAuditTrail(session['saccomember']['fname'], session['saccomember']['email'], action, data)

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
            next_of_kin_name, 
            date_of_birth,
            password
            ) 
    
    def deleteMembers(self):
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

        return saccomemberRepo.deleteSaccoMembers(rows, session['saccomember'], action, oldData)
    
    def updateMember(self):
        id = request.form.get("id")
        sacco_id = request.form.get("sacco_id")
        account_number = request.form.get("account_number")
        fname = request.form.get("fname")
        lname = request.form.get("lname")
        gender = request.form.get("gender")
        phone = request.form.get("phone")
        email = request.form.get("email")
        role = request.form.get("role")
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

        
        
            
        return saccomemberRepo.updateSaccoMember(id, sacco_id, account_number, fname, lname, gender, phone, email, role, next_of_kin_name, date_of_birth, session['saccomember'], action, oldData)
    

   



   
        
            

