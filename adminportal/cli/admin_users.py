from flask_mysqldb import MySQL 
import MySQLdb.cursors
import hashlib
import click
from getpass import getpass

class AdminUserOpps():
    app=None
    db=None
    def __init__(self, app):
        self.app = app
        self.db = MySQL(app)
    
    def create_user(self):
        

        try:
            cursor = self.db.connection.cursor(MySQLdb.cursors.DictCursor)
        except:
            print(f"Failed to connect to DB {self.app.config['MYSQL_HOST']} {self.app.config['MYSQL_USER']}")
            quit()

        name = ""
        email = ""
        phone = ""
        password = ""

        while True:
            if len(name) < 1:
                name = input("Enter the admin's name or 'q' to quit: ")
                if name == "q":
                    print("Closing...")
                    quit()
                if len(name) < 1:
                    continue
            
            if len(email) < 1:
                email = input("Enter the admin's email address or 'q' to quit: ")
                if email == "q":
                    print("Closing...")
                    quit()
                if len(email) < 1:
                    continue

            if len(phone) < 1:
                phone = input("Enter the admin's phone or 'q' to quit: ")
                if phone == "q":
                    print("Closing...")
                    quit()
                if len(phone) < 1:
                    continue

            if len(password) < 1:
                password = getpass("Enter the admin's password or 'q' to quit: ")
                if password == "q":
                    print("Closing...")
                    quit()
                if len(password) < 1:
                    continue

            break



        cursor.execute(
            '''SELECT * FROM user WHERE email= %(email)s ''', 
            {'email':email}
        )
        user = cursor.fetchone()
        if user:
            sql = ''' 
                UPDATE `user` SET `name`=%s, password = %s 
            '''
            cursor.execute(sql, (name, hashlib.sha256(password.encode()).hexdigest()))
            cursor.connection.commit()
        else:
            sql = ''' 
                INSERT INTO `user` SET `name`=%s, `email`=%s, phone=%s, password = %s 
            '''
            cursor.execute(sql, (name, email, phone, hashlib.sha256(password.encode()).hexdigest()))
            cursor.connection.commit()

        print("You have suuccessfully updated your user")