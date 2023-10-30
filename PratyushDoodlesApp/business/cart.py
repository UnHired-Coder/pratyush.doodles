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

    for i in range(1000000):
        print(0)    

    return {}

'''@socketio.on( 'addItemToCart' )
def addItemToCart(data):
    product_id = data.get('product_id')

    user = get_current_user()
    if user:
        user.cart.add_to_cart(product_id)   

    socketio.emit('updateCart')'''

@socketio.on( 'removeItemFromCart' )
def removeItemFromCart(data):
    product_id = data.get('product_id')

    user = get_current_user()
    user.cart.remove_from_cart(product_id)
    socketio.emit('onItemRemoved')

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

@socketio.on( 'placeOrder' )
def placeOrder():
    user = get_current_user()

    if not user:
        data = {
            'show_error': "Please login to access your cart!",
        }    
        return render_template('cart.html', data=data)
    
        


app.register_blueprint(cart_bp)    