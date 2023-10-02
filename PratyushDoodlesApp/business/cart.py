from flask import render_template
from flask import Blueprint
from .. import app
from ..models.UserModel import Cart
from ..models.ProductModel import Product
from .util import *



cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/cart')
def cart():
    user = get_current_user()
    cart = Cart.query.filter_by(user_id=1).first()

    cart_items = []

    for item in cart.cart_items:
        product = Product.query.filter_by(id = item.product_id).first()
        cart_items.append({
            'product':product,
            'quantity':item.quantity
        })

    data = {
        'user': user,
        'cart_items': cart_items
    }

    return render_template('cart.html', data=data)


app.register_blueprint(cart_bp)    