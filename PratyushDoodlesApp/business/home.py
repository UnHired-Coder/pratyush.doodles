from flask import render_template, session
from flask import Blueprint
from .. import app
from flask_dance.contrib.google import google
from ..models.UserModel import User
from .util import *


home_bp = Blueprint('home', __name__)

'''@home_bp.route('/home', methods=['GET'])
@home_bp.route('/home/', methods=['GET'])
def home():
    user = get_current_user()
    data = {
        'user': user
    }

    return render_template('index.html', data = data)'''

@home_bp.route('/orders', methods=['GET'])
@home_bp.route('/orders/', methods=['GET'])
def orders():
    user = get_current_user()

    orders = user.ger_orders()
    data = {
        'user': user,
        'orders': orders
    }

    return render_template('orders.html', data = data)

app.register_blueprint(home_bp)