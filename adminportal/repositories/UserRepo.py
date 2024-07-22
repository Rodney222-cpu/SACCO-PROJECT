from flask_mysqldb import MySQL 
import MySQLdb.cursors
import hashlib
from flask_babel import _
from .MessagesRepo import getMessages


class UserRepo():
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
    def getUserByName(self, name):
        
        try:
            cursor = self.db.connection.cursor(MySQLdb.cursors.DictCursor)
        except Exception:
            return {'status':"ERROR", "message":f"Exception: {Exception}"}
        

        cursor.execute(
            '''SELECT * FROM `user` WHERE name= %(name)s ''', 
            {'email':name}
        )
        user = cursor.fetchone()
        return user
    
    '''
    @Param String username      This is the username of the user
    
    Return Dictionry(id,name,email...updated)
    '''
    def getUserByUsername(self, username):
        
        try:
            cursor = self.db.connection.cursor(MySQLdb.cursors.DictCursor)
        except Exception:
            return {'status':"ERROR", "message":f"Exception: {Exception}"}
        

        cursor.execute(
            '''SELECT * FROM `user` WHERE email= %(email)s ''', 
            {'email':username}
        )
        user = cursor.fetchone()
        return user
