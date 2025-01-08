from flask_babel import _
from flask import(session, redirect,render_template,request)
from flask import current_app
from ...repositories.MessagesRepo import getMessages
from ...repositories.MembersRepo import MembersRepo
from ...appmodules.auth.ControllerAuth import ControllerAuth





class ControllerMembers():
    app=None
    db=None
    messages=None
    def __init__(self, app):
        self.app=app
        self.db=app.db
        self.messages =getMessages(app)
        self.authenticate = ControllerAuth(app)

    def index(self):
        messages = getMessages(app=self.app)
        if 'username' not in session:
            return {
                "status_code": "001",
                "status":"ERROR",
                "messages":_("%(msg)s", msg=messages['invalid_username'])
            }
        
        return {
            "status_code":"000",
            "status":"OK",
            "html":render_template('members/members_table.html', messages=getMessages(app=self.app)),
            "js":render_template('members/members.js', messages=getMessages(app=self.app))
        }

