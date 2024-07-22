from flask_babel import _
from flask import (session,request,redirect, render_template)
from flask import current_app
import hashlib
from ...repositories.MessagesRepo import getMessages
from ...repositories.UserRepo import UserRepo

class ControllerAcg():
    app=None
    db=None
    messages=None
    def __init__(self, app):
        self.app = app
        self.db = app.db
        self.messages = getMessages(app)

    def index(self):
        messages=getMessages(app=self.app)
        if 'username' not in session:
            return {
                "status_code" : "001",
                "status": "ERROR",
                "message":_("%(msg)s ", msg=messages['invalid_username'])
            }

        return {
            "status_code":"000",
            "status":"OK",
            "html":render_template('acgs/acgs_table.html', messages=getMessages(app=self.app)),
            "js":render_template('acgs/acgs.js', messages=getMessages(app=self.app)),    
        }