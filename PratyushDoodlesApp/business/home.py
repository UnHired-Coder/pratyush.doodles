from flask import render_template, session
from flask import Blueprint
from .. import app
from flask_dance.contrib.google import google
from ..models.UserModel import User
from .util import *


home_bp = Blueprint('home', __name__)

@home_bp.route('/')
@home_bp.route('/home')
def home():
    user = get_current_user()

    data = {}
    if not user:
        data = {
            'show_error': "Logged out!",
        }
    else:
        data = {
            'user': user
        }

    return render_template('index.html', data = data)

app.register_blueprint(home_bp)