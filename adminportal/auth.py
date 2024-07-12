from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
import json
import os

app = None
bp = Blueprint('auth', __name__)

@bp.route('/', methods=('GET', 'POST'))
@bp.route('/login', methods=('GET', 'POST'))
def index():
    return render_template('auth/login.html', messages=get_messages())

def get_messages():
    messages = {}
    messages_file = os.path.join(app.root_path, 'messages.json')
    with open(messages_file) as messages_file:
        messages = json.load(messages_file)
        return messages
    
def setAppInstance(appInstance):
    global app
    app = appInstance