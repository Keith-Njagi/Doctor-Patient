import os
from datetime import timedelta

from flask import Flask, session

from models import db
from views import csrf, login_manager

app = Flask(__name__)

class Config(object):
    SECRET_KEY = 'randomsecret'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False     

class Development(Config):
    ENVIRONMENT = 'Development'
    DEBUG = True


app.config.from_object(Development)                   

basedir = os.path.abspath(os.path.dirname(__file__))
 
db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

# csrf.init_app(app)
login_manager.init_app(app)

login_manager.login_view = 'login'
login_manager.login_message = u"Log in to access more resources."
login_manager.login_message_category = "info"
login_manager.refresh_view = 'login'
login_manager.needs_refresh_message = u"Session timedout, please login again"
login_manager.needs_refresh_message_category = "info"

app.app_context().push()

@app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=30)


from views.auth import *
from views.user_views import *
from views.doctor_views import *


if __name__ == '__main__':
    app.run()
