from flask import Flask, session
from routes import routes
from flask_session import Session
from models import str_random
import os

app = Flask(__name__)
app.register_blueprint(routes)
SECRET_KEY = os.urandom(32)
app.secret_key = SECRET_KEY
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
