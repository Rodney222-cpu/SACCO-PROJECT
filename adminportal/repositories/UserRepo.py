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
    @Param String username      This is the username
    @Param String password      This is the user's password

    Dictionary {stat,message}
    '''
    def authenticate_user(self, username, password):
        
        try:
            cursor = self.db.connection.cursor(MySQLdb.cursors.DictCursor)
        except Exception:
            return {'status':"ERROR", "message":f"Exception: {Exception}"}
        

        cursor.execute(
            '''SELECT * FROM `user` WHERE email= %(email)s ''', 
            {'email':username}
        )
        user = cursor.fetchone()
        if not user:
            return {'status':"ERROR", "message":_('%(msg)s', msg=self.messages['error_user_not_exist'])}
        else:
            #Check user's password
            hashed_pw = hashlib.sha256(password.encode()).hexdigest()
            if user['password'] == hashed_pw:
                return {'status':"OK", "message":_('%(msg)s', msg=self.messages['user_authenticated'])}
           
            else:
                return {'status':"ERROR", "message":_('%(msg)s', msg=self.messages['pass_auth_failed'])}


    '''
    @Param String username      This is the username of the user
    
    Return Dictionry(id,name,email...updated)
    '''
    def getUserByName(self, username):
        
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
