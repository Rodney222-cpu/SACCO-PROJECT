from flask_mysqldb import MySQL
import MySQLdb.cursors
from flask_babel import _
from .MessagesRepo import getMessages


class MemberCompletedTransactionsRepo():
    app=None
    db=None
    messages=None
    def __init__(self, app):
        self.app = app
        self.db = app.db
        self.messages = getMessages(app)

    
    def addMemberCompletedTransaction(self, member_id, transaction_log_id, narrative, amount, balance_before, balance_after):
        try:
            cursor = self.db.connection.cursor(MySQLdb.cursors.DictCursor)
        except Exception:
            return {'status':"ERROR", "message":f"Exception: {Exception}"}

        cursor.execute(
            '''INSERT INTO `member_completed_transactions`(member_id, transaction_log_id, narrative, amount, balance_before, balance_after)
               VALUES(%(member_id)s, %(transaction_log_id)s, %(narrative)s, %(amount)s, %(balance_before)s, %(balance_after)s )''',
               {
                   'member_id':member_id,
                   'transaction_log_id':transaction_log_id,
                   'narrative':narrative,
                   'amount':amount,
                   'balance_before':balance_before,
                   'balance_after':balance_after
               }
        )
        self.db.connection.commit()
        return{'status':"OK", "message":self.messages['transaction_created_successfully']}    