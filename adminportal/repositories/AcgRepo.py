from flask_mysqldb import MySQL 
import MySQLdb.cursors
from flask_babel import _
from .MessagesRepo import getMessages
from ..repositories.AuditTrailRepo import AuditTrailRepo


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
    @Param Int id               This is the id of the acg
    @Param String name          This is the name of the acg
    @Param List privileges      A list of privilege names
    @Param user                 A dictionary with user's attributes.
    @Param action               This is the description of the action to be stored in audit tail
    @Param oldData              A string of old acg data that was replaced with the new records

    Return Dictionry(id,name...updated_on)
    '''
    def updateAcg(self, id, name, privileges, user, action, oldData):
        
        try:
            cursor = self.db.connection.cursor(MySQLdb.cursors.DictCursor)
        except Exception:
            return {'status':"ERROR", "message":f"Exception: {Exception}"}
        
        try:
            cursor.execute(
                '''UPDATE `acg` SET name= %(name)s WHERE id=%(id)s''', 
                {'name':name, 'id':id}
            )
            acg_id = id

            cursor.execute(
                '''DELETE FROM `acg_privilege` WHERE acg_id=%(id)s''', 
                {'id':id}
            )

            for privilege in privileges:
                cursor.execute(
                    '''INSERT INTO `acg_privilege` SET acg_id=%(acg_id)s, privilege_name=%(name)s ''', 
                    {'acg_id':acg_id,'name':privilege}
                )
                
                
            AuditTrailRepo.addAuditTrailWithCursor(user['name'], user['email'], action, oldData, cursor)
            
        except TypeError as e:
            cursor.connection.rollback()
            return {'status':"ERROR", "message":f"Exception: {e}"}
        
        cursor.connection.commit()
        return {'status':"OK", "message":self.messages['acg_updated_successfully']}
    
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

    def getOneAcgById(self, id):
        try:
            cursor = self.db.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(
                '''SELECT * FROM `acg` WHERE id= %(id)s ''', 
                {'id':id}
            )
            acg = cursor.fetchone()
            return acg
        except Exception:
            return {'status':"ERROR", "message":f"Exception: {Exception}"}
        
        

    def getAcgs(self):
        try:
            cursor = self.db.connection.cursor(MySQLdb.cursors.DictCursor)
        except Exception:
            return {'status':"ERROR", "message":f"Exception: {Exception}"}
        
        cursor.execute(
            '''SELECT * FROM `acg` ''', 
            {}
        )
        allAcgs = cursor.fetchall()
        allAcgsList = list(allAcgs)
        i=0
        for acg in allAcgs:
            cursor.execute(
                '''SELECT * FROM `acg_privilege` WHERE acg_id=%(acg_id)s ''', 
                {"acg_id":acg['id']}
            )
            acg["acg_privileges"] = cursor.fetchall()
            allAcgsList[i] = acg
            i +=1
        return allAcgsList   
    
    
    def deleteAcg(self, name):
        try:
            cursor = self.db.connection.cursor(MySQLdb.cursors.DictCursor)
        except Exception:
            return {'status':"ERROR", "message":f"Exception: {Exception}"}
        
        sql = ''' 
                DELETE FROM `acg_privilege` WHERE `acg_id`=%s AND 'privilege_name'=%s 
            '''
        try:
            cursor.execute(sql, (name))
            cursor.connection.commit()
        except Exception:
            self.db.connection.rollback()
            return {'status':"ERROR", "message":f"Exception: {Exception}"}
        
        return {'status':"OK", "message":self.messages['acg_deleted']}



    def deleteAcgs(self, rows, user, action, oldData):
        try:
            cursor = self.db.connection.cursor(MySQLdb.cursors.DictCursor)
        except Exception:
            return {'status':"ERROR", "message":f"Exception: {Exception}"}
        
        try:
            for acg in rows:
                
                cursor.execute(
                    '''DELETE FROM `acg` WHERE `id`=%(id)s ''', {"id":acg['id']}
                )
                
            AuditTrailRepo.addAuditTrailWithCursor(user['name'], user['email'], action, oldData, cursor)
  
            cursor.connection.commit()
        except self.db.Error as e:
            try:
                self.db.connection.rollback()
                return {'status':"ERROR", "message":"MySQL Error [%d]: %s" % (e.args[0], e.args[1])}
            except IndexError:
                return {'status':"ERROR", "message":"MySQL Error: %s" % str(e)}

        return {'status':"OK", "message":self.messages['acg_deleted']}
    