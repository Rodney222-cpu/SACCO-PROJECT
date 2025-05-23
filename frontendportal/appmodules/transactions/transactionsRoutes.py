from flask import (
    Blueprint,session,redirect,render_template,request
)
from flask_babel import _
from flask_babel import Babel
from ...repositories.MessagesRepo import getMessages
from ...repositories.TransactionsRepo import TransactionsRepo
import logging
from flask import current_app
from .ControllerTransactions import ControllerTransactions
transactions_bp = Blueprint('transactions', __name__)

#logger = logging.getLogger(_name_)

@transactions_bp.route('/transactions', methods=('GET', 'POST'))
def index():
    controllerTransactions = ControllerTransactions(current_app)
    return controllerTransactions.index()

@transactions_bp.route('/getTransactions', methods=('GET', 'POST'))
def getTransactions():
    controllerTransactions = ControllerTransactions(current_app)
    return controllerTransactions.getTransactions()

@transactions_bp.route('/addTransactions', methods=('GET', 'POST'))
def addTransaction():
    controllerTransactions = ControllerTransactions(current_app)
    return controllerTransactions.addTransaction()   

