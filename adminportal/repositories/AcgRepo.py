from flask_mysqldb import MySQL 
import MySQLdb.cursors
from flask_babel import _
from .MessagesRepo import getMessages


class AcgRepo():
    app=None
    db=None
    messages=None
    def __init__(self, app):
        self.app = app
        self.db = app.db
        self.messages = getMessages(app)

    '''
    @Param String name          This is the name of the acg
    @Param List privileges      A list of privilege names
    
    Return Dictionry(id,name,email...updated)
    '''
    def addAcg(self, name, privileges):
        
        try:
            cursor = self.db.connection.cursor(MySQLdb.cursors.DictCursor)
        except Exception:
            return {'status':"ERROR", "message":f"Exception: {Exception}"}
        
        try:
            cursor.execute(
                '''INSERT INTO `acg` SET name= %(name)s ''', 
                {'name':name}
            )
            acg_id = cursor.lastrowid

            for privilege in privileges:
                cursor.execute(
                    '''INSERT INTO `acg_privilege` SET acg_id=%(acg_id)s, privilege_name=%(name)s ''', 
                    {'acg_id':acg_id,'name':privilege}
                )
                
            
        except TypeError as e:
            cursor.connection.rollback()
            return {'status':"ERROR", "message":f"Exception: {e}"}
        
        cursor.connection.commit()
        return {'status':"OK", "message":self.messages['acg_created_successfully']}
    
    '''
    deleteAcgByName deletes acg by name.

    @Param String name      This is the name of the acg.
    
    Returns Dictionary {status,message}
    '''
    def deleteAcgByName(self, name):
        try:
            cursor = self.db.connection.cursor(MySQLdb.cursors.DictCursor)
        except Exception:
            return {'status':"ERROR", "message":f"Exception: {Exception}"}
        
        sql = ''' 
                DELETE FROM `acg` WHERE `name`=%s 
            '''
        try:
            cursor.execute(sql, (name))
            cursor.connection.commit()
        except Exception:
            return {'status':"ERROR", "message":f"Exception: {Exception}"}
        
        return {'status':"OK", "message":self.messages['acg_deleted']}
    

    def getOneAcgByName(self, name):
        try:
            cursor = self.db.connection.cursor(MySQLdb.cursors.DictCursor)
        except Exception:
            return {'status':"ERROR", "message":f"Exception: {Exception}"}
        
        cursor.execute(
            '''SELECT * FROM `acg` WHERE name= %(name)s ''', 
            {'name':name}
        )
        acg = cursor.fetchone()