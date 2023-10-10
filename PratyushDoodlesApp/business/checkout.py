from flask import render_template
from flask import Blueprint
from .. import app
from .util import *


checkout_bp = Blueprint('checkout', __name__)

# Define routes and views for the 'auth' Blueprint
@checkout_bp.route('/checkout')
def checkout():
    user = get_current_user()
    data = {
        'user': user
    }
    return render_template('checkout.html', data=data)

app.register_blueprint(checkout_bp)