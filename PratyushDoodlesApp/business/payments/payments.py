from flask import render_template
from flask import Blueprint

payments_bp = Blueprint('payments', __name__)

# Define routes and views for the 'auth' Blueprint
@payments_bp.route('/payments')
def payments():
    return render_template('payments.html')