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
    @Param String username      This is the username of the user
    
    Return Dictionry(id,name,email...updated)
    '''
    def getSaccoMemberBySaccoId(self, sacco_id):

        try:
            cursor = self.db.connection.cursor(MySQLdb.cursors.DictCursor)
        except Exception:
             return {'status':"ERROR", "message":f"Exception: {Exception}"}

        cursor.execute(
            '''SELECT * FROM `sacco_member` WHERE sacco_id= %(sacco_id)s''',
            {'sacco_id':sacco_id}
        )
        saccomember = cursor.fetchone()
        return saccomember        


    '''
    Used to obtain a SACCO member by sacco_id and member's account number
    @Param String sacco_id                  This is the id of the sacco.
    @Param String account_number            This is the member's account number.
    
    Return Dictionry(id,name,email...updated)
    '''
    def getSaccoMemberBySaccoIdAndAccNumber(self, sacco_id, accNumber):
        try:
            cursor = self.db.connection.cursor(MySQLdb.cursors.DictCursor)
        except Exception:
             return {'status':"ERROR", "message":f"Exception: {Exception}"}

        cursor.execute(
            '''SELECT * 
            FROM 
                `sacco_member` 
            WHERE 
                sacco_id= %(sacco_id)s 
                AND account_number= %(accNumber)s
            ''',
            {'sacco_id':sacco_id, 'account_number':accNumber}
        )
        saccomember = cursor.fetchone()
        return saccomember 


    '''
    Used to obtain a SACCO member by sacco_id and member's account number
    @Param String sacco_id                  This is the id of the sacco.
    @Param String username                  This can be an email or phone.
    
    Return Dictionry(id,name,email...updated)
    '''
    def getSaccoMemberBySaccoIdAndUsername(self, sacco_id, username):
        try:
            cursor = self.db.connection.cursor(MySQLdb.cursors.DictCursor)
        except Exception:
             return {'status':"ERROR", "message":f"Exception: {Exception}"}

        cursor.execute(
            '''SELECT * 
            FROM 
                `sacco_member` 
            WHERE 
                sacco_id= %(sacco_id)s 
                AND (phone=%(username)s || email = %(username)s)
            ''',
            {'sacco_id':sacco_id, 'username':username}
        )
        saccomember = cursor.fetchone()
        return saccomember   
    
    
    def getSaccoMembers(self, id):
        try:
            cursor = self.db.connection.cursor(MySQLdb.cursors.DictCursor)
        except Exception:
            return {"status":"ERROR", "message":f"Exception: {Exception}"}
        
        cursor.execute(
            '''SELECT * FROM `sacco_member` WHERE sacco_id = %(sacco_id)s''',
            {"sacco_id":id}
        )
        return cursor.fetchall()
       

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
            '''INSERT INTO `sacco_member`(sacco_id, account_number, fname, lname, gender, phone, email, role, next_of_kin_name, date_of_birth, password)
               VALUES(%(sacco_id)s, %(account_number)s, %(fname)s, %(lname)s, %(gender)s, %(phone)s, %(email)s, %(role)s, %(next_of_kin_name)s, %(date_of_birth)s, %(password)s)''',
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
 
    def getOneSaccoMemberByEmail(self, email):
        try:
            cursor =self.db.connection.cursor(MySQLdb.cursors.DictCursor)
        except Exception:
            return {'status':"ERROR", "message":f"Exception: {Exception}"}
        
        cursor.execute(
           '''SELECT * FROM `sacco_member` WHERE email = %(email)s''',
            {'email':email}
        )
        saccomember = cursor.fetchone()
        
        if saccomember:
            return {'status':"ERROR", "message":"Sacco Member with this email already exists"}
        
        return saccomember
    

    def deleteSaccoMembers(self, rows, saccomember, action, oldData):
        try:
            cursor = self.db.connection.cursor(MySQLdb.cursors.DictCursor)
        except Exception:
            return {'status':"ERROR", "message":f"Exception: {Exception}"}
        
        try:
            for saccomember in rows:
                
                cursor.execute(
                    '''DELETE FROM `sacco_member` WHERE `id`=%(id)s ''', {"id":saccomember['id']}
                )

                AuditTrailRepo.addAuditTrailWithCursor(saccomember['fname'], saccomember['email'], action, oldData, cursor)
            
           
            cursor.connection.commit()

        except MySQLdb.Error as e:
            try:
                self.db.connection.rollback()
                return {'status':"ERROR", "message":"MySQL Error [%d]: %s" % (e.args[0], e.args[1])}
            except IndexError:
                return {'status':"ERROR", "message":"MySQL Error: %s" % str(e)}


        return {'status':"OK", "message":self.messages['sacco_member_deleted']}
    
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

    def updateSaccoMember(self, id, sacco_id, account_number, fname, lname, gender, phone, email, role, next_of_kin_name, date_of_birth, saccomember, action, oldData):
        
        try:
            cursor = self.db.connection.cursor(MySQLdb.cursors.DictCursor)
        except Exception:
            return {'status':"ERROR", "message":f"Exception: {Exception}"}
        
        try:
            cursor.execute(
                '''UPDATE `sacco_member` SET  sacco_id= %(sacco_id)s, account_number= %(account_number)s, fname=%(fname)s, lname=%(lname)s, gender=%(gender)s, phone=%(phone)s, email=%(email)s, role=%(role)s, next_of_kin_name=%(next_of_kin_name)s, date_of_birth=%(date_of_birth)s WHERE id=%(id)s''', 
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

            AuditTrailRepo.addAuditTrailWithCursor(saccomember['fname'], saccomember['email'], action, oldData, cursor)    
            
        except TypeError as e:
            cursor.connection.rollback()
            return {'status':"ERROR", "message":f"Exception: {e}"}
        
        cursor.connection.commit()
        return {'status':"OK", "message":self.messages['sacco_member_updated_successfully']}
    
    
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


    def getOneSaccoMemberByPhone(self, member_id):
        try:
            cursor = self.db.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(
                '''SELECT * FROM `sacco_member` WHERE id =%(member_id)s''',
                {'member_id':member_id} 
            )
            saccomember = cursor.fetchone()
            return saccomember
        except Exception:
            return {'status':"ERROR", "message":f"Exception: {Exception}"}   
          
    
    
    def updateMemberBalance(self, member_id, balance_after):
        try:
            cursor = self.db.connection.cursor(MySQLdb.cursors.DictCursor)
        except Exception:
            return {'status':"ERROR", "message":f"Exception: {Exception}"}
        
        try:
            cursor.execute(
                '''UPDATE `sacco_member` SET balance = %(balance_after)s WHERE id = %(member_id)s''',
                {'balance_after':balance_after, 
                'member_id':member_id
                }
            )
            cursor.connection.commit()
            return {'status':"OK", "message":self.messages['balance_updated_successfully']}
        except TypeError as e:
            cursor.connection.rollback()
            return {'status':"ERROR", "message":f"Exception: {e}"}
    
      




