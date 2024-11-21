from flask_mysqldb import MySQL
import MySQLdb.cursors
from flask_babel import _
from .MessagesRepo import getMessages

class AuditTrailRepo():
    app=None
    db=None
    messages=None
    def __init__(self, app):
        self.app=app
        self.db=app.db
        self.messages=getMessages(app)



    def getAuditTrails(self):
        try:
            cursor = self.db.connection.cursor(MySQLdb.cursors.DictCursor)
        except Exception:
            return {'status':"ERROR", "message":f"Exception: {Exception}"}
        
        cursor.execute(
            '''SELECT * FROM `audit_trail` ''', 
            {}
        )
        allAuditTrail = cursor.fetchall()
        allAuditTrailList = list(allAuditTrail)
       
        return allAuditTrailList   
    


    def addAuditTrail(self, user_name, email, action, data):
        try:
            cursor = self.db.connection.cursor(MySQLdb.cursors.DictCursor)
        except Exception:
            return {'status':"ERROR", "message":f"Exception: {Exception}"}

        cursor.execute(
            '''INSERT INTO `audit_trail` 
            SET `user_name`=%(user_name)s, `email`=%(email)s, 
            `action`=%(action)s, `data`=%(data)s''',
            {'user_name':user_name, 'email':email, 'action':action, 'data':data}
        ) 

        self.db.connection.commit()
        return {'status':"OK", "message":"Audit Trail added successfully"}  


    def addAuditTrailWithCursor(user_name, email, action, data, cursor):
        
        cursor.execute(
            '''INSERT INTO `audit_trail` 
            SET `user_name`=%(user_name)s, `email`=%(email)s, 
            `action`=%(action)s, `data`=%(data)s''',
            {'user_name':user_name, 'email':email, 'action':action, 'data':data}
        ) 

        return {'status':"OK", "message":"Audit Trail added successfully"}  
        