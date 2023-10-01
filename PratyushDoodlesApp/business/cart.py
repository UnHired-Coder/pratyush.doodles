from flask import render_template
from flask import Blueprint
from .. import app

cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/cart')
def cart():

    data = {
        'title': "no name"
    }

    return render_template('cart.html', data=data)


app.register_blueprint(cart_bp)    