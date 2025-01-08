from flask_mysqldb import MySQL 
import MySQLdb.cursors
from flask_babel import _
from .MessagesRepo import getMessages


class MembersRepo():
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
    def membersWithEmailAndNotId(self, email, id):
        
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

    
    def getOneMemberById(self, id):
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
          
    
    def getMembers(self, sacco_id):
        try:
            cursor = self.db.connection.cursor(MySQLdb.cursors.DictCursor)
        except Exception:
            return {'status':"ERROR", "message":f"Exception: {Exception}"}
        
        cursor.execute(
            '''SELECT * FROM sacco_member''',
            {}
            
        )
        allSaccoMember = cursor.fetchall()
        
        i=0
        for saccoMember in allSaccoMember:
            cursor.execute(
               '''SELECT * FROM `sacco_member` WHERE sacco_id = %(sacco_id)s ''', 
            {"sacco_id":sacco_id}  
            )
            i +=1
        return allSaccoMember    
    
    
    def getOneMemberByEmail(self, email):
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
         

    def getMemberById(self, id):
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


    def memberEmailAndNotId(self, email, id):
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


           
    
    

          


    
  

         
  

       
              
       
       
        
        