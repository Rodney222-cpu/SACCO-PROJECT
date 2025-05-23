from flask_mysqldb import MySQL 
import MySQLdb.cursors
import hashlib
from flask_babel import _
from .MessagesRepo import getMessages
from ..repositories.AuditTrailRepo import AuditTrailRepo


class SaccoMemberRepo():
    app=None
    db=None
    messages=None
    def __init__(self, app):
        self.app = app
        self.db = app.db
        self.messages = getMessages(app)

    '''
    @Param String name      This is the name of the user
    
    Return Dictionry(id,name,email...updated)
    '''
    

    '''
    @Param String email      This is the email
    
    Return Dictionry(id,name,email...updated)
    '''
    def saccomemberWithEmailAndNotId(self, email, id):
        
        try:
            cursor = self.db.connection.cursor(MySQLdb.cursors.DictCursor)
        except Exception:
            return {'status':"ERROR", "message":f"Exception: {Exception}"}
        

        cursor.execute(
            '''SELECT * FROM `sacco_member` WHERE email= %(email)s AND id <> %(id)s ''', 
            {'email':email, 'id':id}
        )
        saccomember = cursor.fetchone()
        return saccomember

    
    def getOneSaccoMemberById(self, id):
        try:
            cursor = self.db.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(
                '''SELECT * FROM `sacco_member` WHERE id= %(id)s ''', 
                {'id':id}
            )
            saccomember = cursor.fetchone()
            return saccomember
        except Exception:
            return {'status':"ERROR", "message":f"Exception: {Exception}"}
          
    
    
    def addSaccoMember(self, sacco_id, account_number, fname, lname, gender, phone, email, role, next_of_kin_name, date_of_birth, password):
        try:
            cursor = self.db.connection.cursor(MySQLdb.cursors.DictCursor)
        except Exception:
            return {'status':"ERROR", "message":f"Exception: {Exception}"}
        
        cursor.execute(
            '''SELECT * FROM `sacco_member` WHERE email= %(email)s  ''', 
            {'email':email}
        )
        saccomember = cursor.fetchone()

        if saccomember:
            return {'status':"ERROR", "message":"Sacco member with this email already exists"}
        
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
       

        cursor.execute(
            '''INSERT INTO `sacco_member`(sacco_id, account_number, fname, lname, gender, phone, email, role,  balance, next_of_kin_name, date_of_birth, password)
               VALUES(%(sacco_id)s, %(account_number)s, %(fname)s, %(lname)s, %(gender)s, %(phone)s, %(email)s, %(role)s, %(balance)s, %(next_of_kin_name)s, %(date_of_birth)s, %(password)s)''',
               {
                   'sacco_id': sacco_id,
                   'account_number': account_number,
                   'fname': fname,
                   'lname': lname,
                   'gender': gender,
                   'phone': phone,
                   'email': email,
                   'role': role,
                   'next_of_kin_name': next_of_kin_name,
                   'date_of_birth': date_of_birth,
                   'password': hashed_password
               }
        )
        
        self.db.connection.commit()
        return {'status':"OK", "message":self.messages['sacco_member_created_successfully']}

    '''
    @Param Int id       This is the primary id of the sacco "sacco.id"
    returns List of sacco member dictionary 
    '''
    def getSaccoMembers(self, id):
        try:
            cursor = self.db.connection.cursor(MySQLdb.cursors.DictCursor)
        except Exception: 
            return {'status':"ERROR", "message":f"Exception: {Exception}"}
        
        cursor.execute(
            '''SELECT * FROM `sacco_member` WHERE sacco_id = %(sacco_id)s''',
            {"sacco_id":id}
            
        )
        return cursor.fetchall()  
        
    def deleteSaccoMembers(self, rows, user, action, oldData):
        try:
            cursor = self.db.connection.cursor(MySQLdb.cursors.DictCursor)
        except Exception:
            return {'status':"ERROR", "message":f"Exception: {Exception}"}
        
        try:
            for saccomember in rows:
                
                cursor.execute(
                    '''DELETE FROM `sacco_member` WHERE `id`=%(id)s ''', {"id":saccomember['id']}
                )
            
            AuditTrailRepo.addAuditTrailWithCursor(user['name'], user['email'], action, oldData, cursor)
            
            cursor.connection.commit()

        except MySQLdb.Error as e:
            try:
                self.db.connection.rollback()
                return {'status':"ERROR", "message":"MySQL Error [%d]: %s" % (e.args[0], e.args[1])}
            except IndexError:
                return {'status':"ERROR", "message":"MySQL Error: %s" % str(e)}


        return {'status':"OK", "message":self.messages['sacco_member_deleted']}
    
    def getOneSaccoMemberByEmail(self, email):
        try:
            cursor = self.db.connection.cursor(MySQLdb.cursors.DictCursor)
        except Exception:
            return {'status': "ERROR", "message":f"Exception: {Exception}"}

        cursor.execute(
            '''SELECT * FROM `sacco_member` WHERE email = %(email)s''',
            {'email':email}
        )
        sacco_member = cursor.fetchone()

        if sacco_member:
            return {'status':"ERROR", "message":"Sacco Member with this email already exists"}   
         

    def getSaccoMemberById(self, id):
        try:
            cursor = self.db.connection.cursor(MySQLdb.cursors.DictCursor)
        except Exception:
            return {'status':"ERROR", "message":f"Exception: {Exception}"} 

        cursor.execute(
            '''SELECT * FROM `sacco_member` WHERE id = %(id)s''',
            {'id': id}
        )  
        saccomember = cursor.fetchone()
        return saccomember


    def saccomemberEmailAndNotId(self, email, id):
        try:
            cursor = self.db.connection.cursor(MySQLdb.cursors.DictCursor)
        except Exception:
            return {'status':"ERROR", "message":f"Exception: {Exception}"}

        cursor.execute(
            '''SELECT * FROM `sacco_member` WHERE email = %(email)s AND id<> %(id)s''',
            {'email':email, 'id': id}
        )
        saccomember = cursor.fetchone()
        return saccomember     


    def updateSaccoMember(self, id, sacco_id, account_number, fname, lname, gender, phone, email, role, next_of_kin_name, date_of_birth, user, action, oldData):
        
        try:
            cursor = self.db.connection.cursor(MySQLdb.cursors.DictCursor)
        except Exception:
            return {'status':"ERROR", "message":f"Exception: {Exception}"}
        
        try:
            cursor.execute(
                '''UPDATE `sacco_member` SET  sacco_id= %(sacco_id)s, account_number= %(account_number)s, fname=%(fname)s, lname=%(lname)s, gender=%(gender)s, phone=%(phone)s, email=%(email)s, role=%(role)s, balance=%(balance)s, next_of_kin_name=%(next_of_kin_name)s, date_of_birth=%(date_of_birth)s WHERE id=%(id)s''', 
                { 
                      'id':id,
                      'sacco_id':sacco_id,
                      'account_number':account_number,
                      'fname':fname,
                      'lname':lname,
                      'gender':gender, 
                      'phone':phone, 
                      'email':email, 
                      'role':role,
                      'next_of_kin_name':next_of_kin_name,
                      'date_of_birth':date_of_birth,
                      
               }
            ) 

            AuditTrailRepo.addAuditTrailWithCursor(user['name'], user['email'], action, oldData, cursor)    
            
        except TypeError as e:
            cursor.connection.rollback()
            return {'status':"ERROR", "message":f"Exception: {e}"}
        
        cursor.connection.commit()
        return {'status':"OK", "message":self.messages['sacco_member_updated_successfully']}
           
    
    

          


    
  

         
  

       
              
       
       
            
  
  
  


                