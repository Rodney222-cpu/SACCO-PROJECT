from flask_mysqldb import MySQL 
import MySQLdb.cursors
import hashlib
from flask_babel import _
from .MessagesRepo import getMessages


class SaccoRepo():
    app=None
    db=None
    messages=None
    def __init__(self, app):
        self.app = app
        self.db = app.db
        self.messages = getMessages(app)

    '''
    @Param String name      This is the name of the sacco
    
    Return Dictionry(group_id,name,location...updated)
    '''
    def getSaccoByName(self, name):
        
        try:
            cursor = self.db.connection.cursor(MySQLdb.cursors.DictCursor)
        except Exception:
            return {'status':"ERROR", "message":f"Exception: {Exception}"}
        

        cursor.execute(
            '''SELECT * FROM `sacco` WHERE name= %(name)s ''', 
            {'name':name}
        )
        sacco = cursor.fetchone()
        return sacco


    '''
    @Param String email      This is the email
    
    Return Dictionry(id,name,email...updated)
    '''
    def saccoWithGroupIdAndNotId(self, group_id, id):
        
        try:
            cursor = self.db.connection.cursor(MySQLdb.cursors.DictCursor)
        except Exception:
            return {'status':"ERROR", "message":f"Exception: {Exception}"}
        

        cursor.execute(
            '''SELECT * FROM `sacco` WHERE group_id= %(group_id)s AND id <> %(id)s ''', 
            {'group_id':group_id, 'id':id}
        )
        sacco = cursor.fetchone()
        return sacco

    '''
    @Param String name      This is the name of the user
    
    Return Dictionry(id,name,email...updated)
    '''
    def getSaccoById(self, id):
        
        try:
            cursor = self.db.connection.cursor(MySQLdb.cursors.DictCursor)
        except Exception:
            return {'status':"ERROR", "message":f"Exception: {Exception}"}
        

        cursor.execute(
            '''SELECT * FROM `sacco` WHERE id= %(id)s ''', 
            {'id':id}
        )
        sacco = cursor.fetchone()
        return sacco
    
    '''
    @Param String username      This is the username of the user
    
    Return Dictionry(id,name,email...updated)
    '''
    
    def addSacco(self,group_id, name, location):
        try:
            cursor = self.db.connection.cursor(MySQLdb.cursors.DictCursor)
        except Exception:
            return {'status':"ERROR", "message":f"Exception: {Exception}"}
        
        cursor.execute(
            '''SELECT * FROM `sacco` WHERE group_id= %(group_id)s  ''', 
            {'group_id':group_id,}
        )
        sacco = cursor.fetchone()

        if sacco:
            return {'status':"ERROR", "message":"Sacco with this group_id already exists"}
        

        cursor.execute(
            '''INSERT INTO `sacco`(group_id, name, location)
               VALUES(%(group_id)s, %(name)s, %(location)s)''',
               {
                   'group_id': group_id,
                   'name': name,
                   'location': location
               }
        )

        
        self.db.connection.commit()
        return {'status':"OK", "message":"Sacco added successfully"}
    

    def getSacco(self):
        try:
            cursor = self.db.connection.cursor(MySQLdb.cursors.DictCursor)
        except Exception:
            return {'status':"ERROR", "message":f"Exception: {Exception}"}
        
        cursor.execute(
            '''SELECT s.*, 
            (SELECT COUNT(*) FROM `sacco_member` WHERE sacco_id = s.id) as total_num_members 
            FROM `sacco` AS s ''', 
            {}
        )
        allSacco = cursor.fetchall()
        allSaccoList = list(allSacco)
       
        return allSaccoList   
    

    def getOneSaccoBySaccoId(self, sacco_id):
        try:
            cursor = self.db.connection.cursor(MySQLdb.cursors.DictCursor)
        except Exception:
            return {'status':"ERROR", "message":f"Exception: {Exception}"}
        
        cursor.execute(
            '''SELECT * FROM `sacco` WHERE group_id= %(sacco_id)s ''', 
            {'sacco_id':sacco_id}
        )
        sacco = cursor.fetchone()

        if not sacco:
            return {'status':"ERROR", "message":"sacco with this group_id does not exist"}
        
        return sacco


    def getOneSaccoByName(self, name):
        try:
            cursor = self.db.connection.cursor(MySQLdb.cursors.DictCursor)
        except Exception:
            return {'status':"ERROR", "message":f"Exception: {Exception}"}
        
        cursor.execute(
            '''SELECT * FROM `sacco` WHERE name= %(name)s ''', 
            {'name':name}
        )
        sacco = cursor.fetchone()


    def deleteSacco(self, rows):
        try:
            cursor = self.db.connection.cursor(MySQLdb.cursors.DictCursor)
        except Exception:
            return {'status':"ERROR", "message":f"Exception: {Exception}"}
        
        try:
            for sacco in rows:
                
                cursor.execute(
                    '''DELETE FROM `sacco` WHERE `id`=%(id)s ''', {"id":sacco['id']}
                )
            
           
            cursor.connection.commit()
        except self.db.Error as e:
            try:
                self.db.connection.rollback()
                return {'status':"ERROR", "message":"MySQL Error [%d]: %s" % (e.args[0], e.args[1])}
            except IndexError:
                return {'status':"ERROR", "message":"MySQL Error: %s" % str(e)}

        return {'status':"OK", "message":self.messages['sacco_deleted']}
    
    
    def updateSacco(self, id, group_id, name, location):
        
        try:
            cursor = self.db.connection.cursor(MySQLdb.cursors.DictCursor)
        except Exception:
            return {'status':"ERROR", "message":f"Exception: {Exception}"}
        
        try:
            cursor.execute(
                '''UPDATE `sacco` SET group_id= %(group_id)s ,name= %(name)s, location= %(location)s WHERE id=%(id)s''', 
                {'group_id':group_id,'name':name, 'location':location, 'id':id}
            )

          
        except TypeError as e:
            cursor.connection.rollback()
            return {'status':"ERROR", "message":f"Exception: {e}"}
        
        cursor.connection.commit()
        return {'status':"OK", "message":self.messages['sacco_updated_successfully']}
    
    def getOneSaccoById(self, id):
        try:
            cursor = self.db.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(
                '''SELECT * FROM `sacco` WHERE id= %(id)s ''', 
                {'id':id}
            )
            sacco = cursor.fetchone()
            return sacco
        except Exception:
            return {'status':"ERROR", "message":f"Exception: {Exception}"}
   
 
     



       
        

    
    
    

    
  

         
  

       
              
       
       
            
  
  
  


                