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
        self.messages = getMessages(app)

    def getTransactions(self, id):
        try:
            cursor = self.db.connection.cursor(MySQLdb.cursors.DictCursor)
        except Exception:
            return {'status':"ERROR", "message":f"Exception: {Exception}"}
        
        cursor.execute(
         '''SELECT t.*, t.member_id, m.sacco_id, m.fname, m.lname
               FROM transaction_log AS t
               LEFT JOIN sacco_member AS m 
               ON t.member_id = m.id
               WHERE t.member_id = %(member_id)s
            ''',
            {"member_id":id}     
        )
        return cursor.fetchall()  
     
    
    def addTransaction(self, sacco_id, member_id, amount, transaction_type, payment_method, narrative, reference, status):
        try:
            cursor = self.db.connection.cursor(MySQLdb.cursors.DictCursor)
        except Exception:
            return {'status':"ERROR", "message":f"Exception: {Exception}"}

        cursor.execute(
            '''SELECT * FROM `transaction_log` WHERE reference = %(reference)s''',
            {'reference':reference}
        ) 
        transaction = cursor.fetchone()

        if transaction:
            return{'status':"ERROR","message":self.messages['transaction_reference_exists'] }
        
        cursor.execute(
            '''INSERT INTO `transaction_log`( sacco_id, member_id, amount, transaction_type, payment_method, narrative, reference, status)
            VALUES( %(sacco_id)s, %(member_id)s, %(amount)s, %(transaction_type)s, %(payment_method)s, %(narrative)s, %(reference)s, %(status)s)''',
            {
                'sacco_id':sacco_id,
                'member_id':member_id,
                'amount':amount,
                'transaction_type':transaction_type,
                'payment_method':payment_method,
                'narrative':narrative,
                'reference':reference,
                'status':status
            }
        )
        transaction_id = cursor.lastrowid
        self.db.connection.commit()
        return{
         'status':"OK",
         'transaction_id':transaction_id, 
         "message":self.messages['transaction_created_successfully']
         }
    
    
    def getTransactionByReference(self, reference):
        try:
            cursor = self.db.connection.cursor(MySQLdb.cursors.DictCursor)
        except Exception:
             return {'status':"ERROR", "message":f"Exception: {Exception}"}
        
        cursor.execute(
            '''SELECT * FROM `transaction_log` WHERE reference = %(reference)s''',
            {'reference':reference}
        )
        transaction = cursor.fetchone()
        return transaction
    

    
           
    
   
            


