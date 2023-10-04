from flask import render_template
from flask import Blueprint
from .. import app
from .util import *


payments_bp = Blueprint('payments', __name__)

# Define routes and views for the 'auth' Blueprint
@payments_bp.route('/payments')
def payments():
    user_id = get_current_user()
    user = User.query.filter_by(id = user_id)
    data = {
        'user': user
    }
    return render_template('payments.html', data=data)

app.register_blueprint(payments_bp)