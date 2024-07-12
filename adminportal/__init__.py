import os

from flask import Flask, request, render_template
from flask_babel import _
from flask_babel import Babel
from flask import url_for
import json

app = None
def get_locale():
    global app
    return request.accept_languages.best_match(app.config['LANGUAGES'])

def create_app():

    global app
    app = Flask(__name__)

    #app.config.from_object('adminportal.default_settings')
    app.config.from_envvar('ADMINPORTAL_SETTINGS')
    
    babel = Babel(app, locale_selector=get_locale)

    from . import auth
    auth.setAppInstance(app)
    app.register_blueprint(auth.bp)
    app.add_url_rule('/', endpoint='index')
    
    return app

