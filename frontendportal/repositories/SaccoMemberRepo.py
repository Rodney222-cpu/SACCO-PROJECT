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
    def getOneSaccoMemberBySaccoId(self, sacco_id):

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