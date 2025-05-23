from flask_mysqldb import MySQL
import MySQLdb.cursors
import hashlib
from flask_babel import _
from .MessagesRepo import getMessages


class TransactionsRepo():
    app=None
    db=None
    messages=None
    def __init__(self, app):
        self.app = app
        self.db = app.db
        self.message = getMessages(app)

    def getTransactions(self):
        try:
            cursor = self.db.connection.cursor(MySQLdb.cursors.DictCursor)
        except Exception:
            return {'status':"ERROR", "message":f"Exception: {Exception}"}
        
        cursor.execute(
            '''SELECT * FROM `transaction_log` ''', 
            {}
        )
        allTransactions = cursor.fetchall()
        allTransactionsList = list(allTransactions)
       
        return allTransactionsList   
            


