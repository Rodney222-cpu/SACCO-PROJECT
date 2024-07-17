from flask import (
    Blueprint, render_template, session, redirect
)
from .repositories.MessagesRepo import getMessages

from flask_babel import _

applayout_bp = Blueprint('applayout', __name__)

@applayout_bp.route('/applayout')
def applayout():
    if 'username' not in session:
        return redirect('/')
        
    return render_template('applayout.html', messages=getMessages(app=applayout_bp))