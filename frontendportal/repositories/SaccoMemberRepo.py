from flask_mysqldb import MySQL
import MySQLdb.cursors
from flask_babel import _
from .MessagesRepo import getMessages



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