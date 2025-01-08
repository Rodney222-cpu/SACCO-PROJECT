import click
from flask.cli import with_appcontext
from flask import Flask
from admin_users import MembersOpps

app = Flask(__name__)
app.config.from_envvar('FRONTENDPORTAL_SETTINGS')

@app.cli.command("create-user")
@with_appcontext
def create_user():
    membersOpps = MembersOpps(app)
    membersOpps.create_user()
    

app.cli.add_command(create_user)