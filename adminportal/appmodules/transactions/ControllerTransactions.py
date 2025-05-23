from flask_babel import _
from flask import(redirect,session,request,render_template)
from flask import current_app
import hashlib
from ...repositories.MessagesRepo import getMessages
from ...repositories.TransactionsRepo import TransactionsRepo
from ...appmodules.auth.ControllerAuth import ControllerAuth

class ControllerTransactions():
    app=None
    db=None
    messages=None
    def __init__(self, app):
        self.app=app
        self.db=app.db
        self.messages= getMessages
        self.authenticate = ControllerAuth(app)

    def index(self):
        messages=getMessages(app=self.app)
        if 'username' not in session:
            return {
                "status_code":"001",
                "status":"ERROR",
                "message":_("%(msg)s", msg=messages['invalid username'])
            }

        return {
            "status_code":"000",
            "status":"OK",
            "html":render_template('transactions/transactions_table.html', messages=getMessages(app=self.app)),
            "js":render_template('transactions/transactions.js', messages=getMessages(app=self.app)),
        }
    
    def getTransactions(self):

        transactionsRepo = TransactionsRepo(current_app)
        transactions = transactionsRepo.getTransactions()

        return {
            "total": len(transactions),
            "rows": transactions
        } 
  


        