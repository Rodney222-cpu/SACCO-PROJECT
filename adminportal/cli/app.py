import click
from flask.cli import with_appcontext
from flask import Flask
from admin_users import AdminUserOpps

app = Flask(__name__)
app.config.from_envvar('ADMINPORTAL_SETTINGS')

@app.cli.command("create-user")
@with_appcontext
def create_user():
    adminUserOpps = AdminUserOpps(app)
    adminUserOpps.create_user()
    

app.cli.add_command(create_user)