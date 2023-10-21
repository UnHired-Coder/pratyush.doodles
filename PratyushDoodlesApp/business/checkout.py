from flask import render_template, Blueprint, jsonify, flash, redirect, url_for
from .. import app, razorpayClient
from .util import *
from .cart import getCartData
from ..forms.ShippingAddressForm import ShippingAddressForm
from .. import socketio
from ..models.UserModel import Address
from .. import db
from flask_wtf import CSRFProtect

checkout_bp = Blueprint('checkout', __name__)
currency = 'INR'

# Define routes and views for the 'auth' Blueprint
@checkout_bp.route('/checkout')
def checkout():
    data = getCartData()
    return render_template('checkout.html', data=data)

# @checkout_bp.route('/initiate_payment', methods=['GET', 'POST'])
def initiate_payment(amount):
    payment_data = {
        'amount': amount,
        'currency': currency,
        'payment_capture': 1
    }

    # Create a Razorpay order
    order = razorpayClient.order.create(data = payment_data)
    order_id = order['id']
    return order_id

@checkout_bp.route( '/getOrderOptions' )
def getOrderOptions():
    data = getCartData()
    if data and data['user']:
        user = data['user']
        amount_payable = data['total_amount']
        order_id = initiate_payment(amount_payable)
        return  {
                    "key": app.config['RAZORPAY_KEY_ID'], 
                    "amount": amount_payable, 
                    "currency": currency,
                    "name": "Pratyush Doodles",
                    "description": "This is sample transaction",
                    "image": "https://example.com/your_logo",
                    "order_id": order_id, 
                    "callback_url": "http://127.0.0.1:5000/payment_callback",
                    "prefill": {
                        "name": user.name,
                        "email": user.email,
                        "contact": user.phone_number
                    },
                    "notes": {
                        "address": "This payment is going to Pratyush Doodles"
                    },
                    "theme": {
                        "color": "#3399cc"
                    }
                }
    return None

@checkout_bp.route('/payment_callback', methods=['POST'])
def payment_callback():
    user = get_current_user()
    user.place_order()
    return user.name

@checkout_bp.route( '/getShippingAddress' )
def getShippingAddress():
    user = get_current_user()
    data = {
        'address' : user.address    
    }

    return render_template('ui/shipping_address.html', data = data)

@socketio.on( 'updateShippingAddress' )
def updateShippingAddress(data):
    errors = []
    form_data = data.get('formData')

    recipient_name = form_data.get('recipient_name', '')
    address_line1 = form_data.get('address_line1', '')
    address_line2 = form_data.get('address_line2', '')
    city = form_data.get('city', '')
    state = form_data.get('state', '')
    postal_code = form_data.get('postal_code', '')
    country = form_data.get('country', '')
    phone_number = form_data.get('phone_number', '')

    if not recipient_name:
        errors.append("Recipient Name is required.")
    if not address_line1:
        errors.append("Address is required.")
    if not city:
        errors.append("City is required.")
    if not state:
        errors.append("State is required.")
    if not postal_code:
        errors.append("Postal Code is required.")
    if not country:
        errors.append("Country is required.")
    if not phone_number:
        errors.append("Phone number is required")    

    if len(errors) > 0:
        response = {'status': 'error', 'errors': errors}
        socketio.emit('error', errors[0])
        return

    user = get_current_user()    
    user.add_or_update_address(recipient_name=recipient_name, addressLine1=address_line1, city=city, state=state, country=country, pincode=postal_code, addressLine2=address_line2, phone_number=phone_number, order_id=None)

    socketio.emit('addressUpdated')

csrf = CSRFProtect(app)
csrf.exempt(checkout_bp)
app.register_blueprint(checkout_bp)