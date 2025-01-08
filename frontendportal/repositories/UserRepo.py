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
            {'name':name}
        )
        user = cursor.fetchone()
        return user


    '''
    @Param String email      This is the email
    
    Return Dictionry(id,name,email...updated)
    '''
    def userWithEmailAndNotId(self, email, id):
        
        try:
            cursor = self.db.connection.cursor(MySQLdb.cursors.DictCursor)
        except Exception:
            return {'status':"ERROR", "message":f"Exception: {Exception}"}
        

        cursor.execute(
            '''SELECT * FROM `user` WHERE email= %(email)s AND id <> %(id)s ''', 
            {'email':email, 'id':id}
        )
        user = cursor.fetchone()
        return user

    '''
    @Param String name      This is the name of the user
    
    Return Dictionry(id,name,email...updated)
    '''
    def getUserById(self, id):
        
        try:
            cursor = self.db.connection.cursor(MySQLdb.cursors.DictCursor)
        except Exception:
            return {'status':"ERROR", "message":f"Exception: {Exception}"}
        

        cursor.execute(
            '''SELECT * FROM `user` WHERE id= %(id)s ''', 
            {'id':id}
        )
        user = cursor.fetchone()
        return user
    
    '''
    @Param String username      This is the username of the user
    
    Return Dictionry(id,name,email...updated)
    '''
    def getUserByUsername(self, email):
        
        try:
            cursor = self.db.connection.cursor(MySQLdb.cursors.DictCursor)
        except Exception:
            return {'status':"ERROR", "message":f"Exception: {Exception}"}
        

        cursor.execute(
            '''SELECT * FROM `user` WHERE email= %(email)s ''', 
            {'email':email}
        )
        user = cursor.fetchone()
        return user
    
    def addUser(self, name, phone, email, password, user_acgs):
        try:
            cursor = self.db.connection.cursor(MySQLdb.cursors.DictCursor)
        except Exception:
            return {'status':"ERROR", "message":f"Exception: {Exception}"}
        
        cursor.execute(
            '''SELECT * FROM `user` WHERE email= %(email)s  ''', 
            {'email':email,}
        )
        user = cursor.fetchone()

        if user:
            return {'status':"ERROR", "message":"User with this email already exists"}
        
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        cursor.execute(
            '''INSERT INTO `user`(name, phone, email, password)
               VALUES(%(name)s, %(phone)s, %(email)s, %(password)s)''',
               {
                   'name': name,
                   'phone': phone,
                   'email': email,
                   'password': hashed_password
               }
        )

        user_id = self.db.connection.insert_id()
        #Adding User ACGs
        for acgId in user_acgs:
            cursor.execute(
                '''INSERT INTO `user_acg`(user_id, acg_id)
                VALUES(%(user_id)s, %(acg_id)s)''',
                {
                    'user_id': user_id,
                    'acg_id': acgId
                }
            )

        self.db.connection.commit()
        return {'status':"OK", "message":"User added successfully"}
    
    def getUser(self):
        try:
            cursor = self.db.connection.cursor(MySQLdb.cursors.DictCursor)
        except Exception:
            return {'status':"ERROR", "message":f"Exception: {Exception}"}
        
        cursor.execute(
            '''SELECT * FROM `user` ''', 
            {}
        )
        allUser = cursor.fetchall()
        allUserList = list(allUser)
        i=0
        for user in allUser:
            cursor.execute(
                '''SELECT * FROM `user_acg` WHERE user_id=%(user_id)s ''', 
                {"user_id":user['id']}
            )
            user["user_acgs"] = cursor.fetchall()
            allUserList[i] = user
            i +=1
        return allUserList   
    
    def getOneUserByEmailAndPhone(self, email, phone):
        try:
            cursor = self.db.connection.cursor(MySQLdb.cursors.DictCursor)
        except Exception:
            return {'status':"ERROR", "message":f"Exception: {Exception}"}
        
        cursor.execute(
            '''SELECT * FROM `user` WHERE email= %(email)s AND phone=%(phone)s''', 
            {'email':email, 'phone':phone}
        )
        user = cursor.fetchone()

        if user:
            return {'status':"ERROR", "message":"User with this email already exists"}

    def getOneUserByName(self, name):
        try:
            cursor = self.db.connection.cursor(MySQLdb.cursors.DictCursor)
        except Exception:
            return {'status':"ERROR", "message":f"Exception: {Exception}"}
        
        cursor.execute(
            '''SELECT * FROM `user` WHERE name= %(name)s ''', 
            {'email':name}
        )
        user = cursor.fetchone()

       
        

    def updateUser(self, user_id, name, phone,  email,  user_acgs):
        
        try:
            cursor = self.db.connection.cursor(MySQLdb.cursors.DictCursor)
        except Exception:
            return {'status':"ERROR", "message":f"Exception: {Exception}"}
        
        try:
            cursor.execute(
                '''UPDATE `user` SET name= %(name)s, phone=%(phone)s, email=%(email)s WHERE id=%(user_id)s''', 
                {'name':name, 'phone':phone, 'email':email, 'user_id':user_id}
            )
            

            cursor.execute(
                '''DELETE FROM `user_acg` WHERE user_id=%(user_id)s''', 
                {'user_id':user_id}
            )

            for acg_id in user_acgs:
               cursor.execute(
                '''INSERT INTO `user_acg` (user_id, acg_id) 
                   VALUES (%(user_id)s, %(acg_id)s)''',
                {'user_id': user_id, 'acg_id': acg_id}
            )
              
           
        except TypeError as e:
            cursor.connection.rollback()
            return {'status':"ERROR", "message":f"Exception: {e}"}
        
        cursor.connection.commit()
        return {'status':"OK", "message":self.messages['user_updated_successfully']}
    
    '''
    deleteUserByName deletes user by name.

    @Param String name      This is the name of the user.
    
    Returns Dictionary {status,message}
    '''

    def deleteUserByName(self, name):
        try:
            cursor = self.db.connection.cursor(MySQLdb.cursors.DictCursor)
        except Exception:
            return {'status':"ERROR", "message":f"Exception: {Exception}"}
        
        sql = ''' 
                DELETE FROM `user` WHERE `name`=%s 
            '''
        try:
            cursor.execute(sql, (name))
            cursor.connection.commit()
        except Exception:
            return {'status':"ERROR", "message":f"Exception: {Exception}"}
        
        return {'status':"OK", "message":self.messages['user_deleted']}

    def deleteUser(self, name):
        try:
            cursor = self.db.connection.cursor(MySQLdb.cursors.DictCursor)
        except Exception:
            return {'status':"ERROR", "message":f"Exception: {Exception}"}
        
        sql = ''' 
                DELETE FROM `user_acg` WHERE `user_id`=%s AND `privilege_name`=%s 
            '''
        try:
            cursor.execute(sql, (name))
            cursor.connection.commit()
        except Exception:
            self.db.connection.rollback()
            return {'status':"ERROR", "message":f"Exception: {Exception}"}
        
        return {'status':"OK", "message":self.messages['user_deleted']}
    
    def deleteUser(self, rows, user, action, oldData):
        try:
            cursor = self.db.connection.cursor(MySQLdb.cursors.DictCursor)
        except Exception:
            return {'status':"ERROR", "message":f"Exception: {Exception}"}
        
        try:
            for user in rows:
                
                cursor.execute(
                    '''DELETE FROM `user` WHERE `id`=%(id)s ''', {"id":user['id']}
                )

            
            cursor.connection.commit()
        except self.db.Error as e:
            try:
                self.db.connection.rollback()
                return {'status':"ERROR", "message":"MySQL Error [%d]: %s" % (e.args[0], e.args[1])}
            except IndexError:
                return {'status':"ERROR", "message":"MySQL Error: %s" % str(e)}

        return {'status':"OK", "message":self.messages['user_deleted']}
    
    def getOneUserById(self, id):
        try:
            cursor = self.db.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(
                '''SELECT * FROM `user` WHERE id= %(id)s ''', 
                {'id':id}
            )
            user = cursor.fetchone()
            return user
        except Exception:
            return {'status':"ERROR", "message":f"Exception: {Exception}"}
   
    

          


    
  

         
  

       
              
       
       
            
  
  
  


                