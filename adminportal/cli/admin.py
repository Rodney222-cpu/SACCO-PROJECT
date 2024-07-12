import click
from flask import Flask
from admin_users import AdminUserOpps

app = Flask(__name__)
app.config.from_envvar('ADMINPORTAL_SETTINGS')

@app.cli.command("create-user")
#@click.argument("")
def create_user():
    adminUserOpps = AdminUserOpps(app)
    adminUserOpps.create_user()
    
