from flask import render_template
from flask import Blueprint
from .. import app, socketio
from ..models.UserModel import Cart
from ..models.ProductModel import Product
from .util import *



cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/cart')
def cart():
    user = get_current_user()

    if not user:
        data = {
            'show_error': "Please login to access your cart!",
        }
        return render_template('cart.html', data=data)


    cart = Cart.query.filter_by(user_id=user.id).first()
    if not cart:
        data = {
            'show_error':"Couldn't load cart!"
        }
        return render_template('cart.html', data=data)


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

@socketio.on( 'addItemToCart' )
def addItemToCart(data):
    product_id = data.get('product_id')

    user = get_current_user()
    if user:
        user.cart.add_to_cart(product_id)

    socketio.emit('updateCart')

@socketio.on( 'removeItemFromCart' )
def removeItemFromCart(data):
    product_id = data.get('product_id')

    user = get_current_user()
    user.cart.remove_from_cart(product_id)

@cart_bp.route('/getCartItems')
def getCartItems():
    # Fetch cart items as a list of objects
    user = get_current_user()
    data = {
        'user' : user
    }

    # Render the Jinja2 template with the cart items
    rendered_template = render_template('cart.html', data=data)
    return rendered_template


@socketio.on( 'placeOrder' )
def placeOrder():
    user = get_current_user()

    if not user:
        data = {
            'show_error': "Please login to access your cart!",
        }    
        return render_template('cart.html', data=data)
    
        


app.register_blueprint(cart_bp)    