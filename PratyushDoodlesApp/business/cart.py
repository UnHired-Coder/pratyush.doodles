from flask import render_template
from flask import Blueprint, request
from .. import app, socketio
from ..models.UserModel import Cart
from ..models.ProductModel import Product
from .util import *

cart_bp = Blueprint('cart', __name__)


@cart_bp.route('/addItemToCart', methods = ['POST'])
def addItemToCart():
    data = request.get_json()
    product_id = data.get('product_id')
    user = get_current_user()
    if user:
        user.cart.add_to_cart(product_id)   
 
    return {}

@cart_bp.route('/reduceItemFromCart', methods = ['POST'])
def reduce_from_cart():
    data = request.get_json()
    product_id = data.get('product_id')
    user = get_current_user()
    if user:
        user.cart.reduce_from_cart(product_id)   
 
    return {}

@cart_bp.route('/removeItemFromCart', methods = ['POST'])
def removeItemFromCart():
    data = request.get_json()
    product_id = data.get('product_id')

    user = get_current_user()
    user.cart.remove_from_cart(product_id)

    return {}

@cart_bp.route('/getCartItemsCount')
def getCartItemsCount():
    data = getCartData()
    return str(data['items_count'])

@cart_bp.route('/getCartItems')
def getCartItems():
    data = getCartData()
    return render_template('cart.html', data=data)

def getCartData():
    # Fetch cart items as a list of objects
    user = get_current_user()
    items_count = 0
    total_amount = 0
    cart_items = None
    if user and user.cart:
        cart_items = user.cart.cart_items
        for cart_item in cart_items:
            items_count = items_count + cart_item.quantity
            
            product = Product.query.filter_by(id = cart_item.product_id).first()
            total_amount = total_amount + (product.price * cart_item.quantity)

    return {
        'user' : user,
        'items_count' : items_count,
        'total_amount' : total_amount,
        'cart_items' : cart_items
    }

app.register_blueprint(cart_bp)    