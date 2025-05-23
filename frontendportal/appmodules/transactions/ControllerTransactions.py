from flask_babel import _
from flask import(redirect,session,request,render_template)
from flask import current_app
from ...repositories.MessagesRepo  import getMessages
from ...repositories.TransactionsRepo import TransactionsRepo
from ...repositories.SaccoMemberRepo import SaccoMemberRepo
from ...repositories.MemberCompletedTransactionsRepo import MemberCompletedTransactionsRepo 
from ...appmodules.auth.ControllerAuth import ControllerAuth
from ...appmodules.apputils.yopayments_util  import YoPayments 
from ...repositories.AuditTrailRepo import AuditTrailRepo

class ControllerTransactions():
    app=None
    db=None
    messages=None
    def __init__(self, app):
        self.app=app
        self.db=app.db                       
        self.messages= getMessages(app)
        self.authenticate = ControllerAuth(app)

    def index(self):
        member_id = request.args.get("member_id")
        messages=getMessages(app=self.app)
        saccomemberRepo = SaccoMemberRepo(current_app)
        saccomember = saccomemberRepo.getSaccoMemberById(member_id)
        if saccomember == None:
            return {
                "status_code":"001",
                "status":"ERROR",
                "message":_("%(msg)s", msg=messages['session_timedout'])
            }

        if 'username' not in session:
            return {
                "status_code":"001",
                "status":"ERROR",
                "message":_("%(msg)s", msg=messages['session_timedout'])
            }


        return {
            "status_code":"000",
            "status":"OK",
            "html":render_template('transactions/transactions_table.html', messages=getMessages(app=self.app), member_id=member_id, saccomember=saccomember),
            "js":render_template('transactions/transactions.js', messages=getMessages(app=self.app),member_id=member_id, saccomember=saccomember),
        }
    
    def getTransactions(self):
        member_id = request.args.get("member_id")
        transactionsRepo = TransactionsRepo(current_app)
        transactions = transactionsRepo.getTransactions(member_id)

        return {
            "total": len(transactions),
            "rows": transactions
        } 
    
    
    def addTransaction(self):
        sacco_id = session['sacco_id']
        member_id = request.form.get('member_id')
        amount = float(request.form["amount"])
        transaction_type = request.form['transaction_type']
        payment_method = request.form['payment_method']
        narrative = request.form['narrative']
        action = f"A {transaction_type} TRANSACTION MADE FROM {member_id}"
        data =""

        transactionRepo = TransactionsRepo(current_app)
        saccomemberRepo = SaccoMemberRepo(current_app)
        auditTrailRepo = AuditTrailRepo(current_app)
        membercompletedtransactionsRepo = MemberCompletedTransactionsRepo(current_app)

        saccomember = saccomemberRepo.getOneSaccoMemberByPhone(member_id)
        if saccomember is None:
            return {
                'status':"ERROR",
                "message":self.messages['member_not_found']
            } 

        msisdn = saccomember.get('phone')

        if msisdn is None:
            return {
                'status':"ERROR",
                "message":self.messages['phone_not_found']
            } 


        balance_before = float(saccomember.get('balance', 0)) 
        balance_after = balance_before

        apiUsername = current_app.config['YO_PAYMENTS_API_USERNAME']
        apiPassword = current_app.config['YO_PAYMENTS_API_PASSWORD']

        yopaymentsObj = YoPayments(apiUsername, apiPassword)

        if transaction_type == "DEPOSIT":
            response = yopaymentsObj.ac_deposit_funds(msisdn, amount, narrative)
        else:
            if balance_before < amount:
                return {'status':"ERROR", 
                        "message":self.messages['insufficient_balance']
                        }
            
            response= yopaymentsObj.ac_withdraw_funds(msisdn, amount, narrative)

        if response.get("Status") == "OK":
            reference = response.get("TransactionReference")
            status = response.get("TransactionStatus")

            balance_after = balance_before + amount if transaction_type == "DEPOSIT" else balance_before - amount

            transaction = transactionRepo.addTransaction(sacco_id, member_id, amount, transaction_type, payment_method, narrative, reference, status)
            if transaction['status'] != "OK":
                return transaction
            
            transaction_log_id = transaction['transaction_id']

            update_balance = saccomemberRepo.updateMemberBalance(saccomember['id'], balance_after)
            if update_balance['status'] !="OK":
                return update_balance
            
            atEntry = auditTrailRepo.addAuditTrail(saccomember['fname']+" "+saccomember['lname'], saccomember['email'], action, data)
            if atEntry['status'] != "OK":
                return atEntry
            
            completed_transactions = membercompletedtransactionsRepo.addMemberCompletedTransaction(member_id, transaction_log_id, narrative, amount, balance_before, balance_after)
            if completed_transactions['status'] != "OK":
                return completed_transactions
            
            return transaction
        else:
            return {
                'status':"ERROR",
                'reference':reference,
                'transaction_status':status,
                "message":self.messages['transaction_failed']
            }
            
                        
           

        
    



    

        

    

       
    

  


        