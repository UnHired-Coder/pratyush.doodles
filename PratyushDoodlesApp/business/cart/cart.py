from flask import render_template
from flask import Blueprint

cart_bp = Blueprint('cart', __name__)

# Define routes and views for the 'auth' Blueprint
@cart_bp.route('/cart')
def cart():

    data = {
        'title': "no name"
    }

    return render_template('cart.html', data=data)