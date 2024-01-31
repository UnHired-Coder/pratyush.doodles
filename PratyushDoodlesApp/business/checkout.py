from flask import render_template, Blueprint, jsonify, flash, redirect, url_for, request
from .. import app, razorpayClient
from .util import *
from .cart import getCartData
from ..forms.ShippingAddressForm import ShippingAddressForm
# from .. import socketio
from ..models.UserModel import Address
from .. import db
# from flask_wtf import CSRFProtect

checkout_bp = Blueprint('checkout', __name__)

currency = 'INR'
shipping_charges = 30
logo_url = "https://stickyshape.pythonanywhere.com/static/images/about_stickers.png"
payment_success_callback = "https://stickyshape.pythonanywhere.com/payment_callback"

# Test Url
# payment_success_callback = "http://127.0.0.1:5000/payment_callback"

@checkout_bp.route('/checkout')
@checkout_bp.route('/checkout/')
def checkout():
    data = getCartData()
    return render_template('checkout.html', data=data)

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

@checkout_bp.route( '/getOrderOptions')
@checkout_bp.route( '/getOrderOptions/')
def getOrderOptions():
    data = getCartData()
    if data and data['user']:
        user = data['user']
        amount_payable = data['total_amount']
        amount_payable_in_paise = (amount_payable + shipping_charges) * 100

        order_id = initiate_payment(amount_payable_in_paise)
        return  {
                    "key": app.config['RAZORPAY_KEY_ID'], 
                    "amount": amount_payable_in_paise, 
                    "currency": currency,
                    "name": "StickyShape.com",
                    "description": "Paying StickyShape.com",
                    "image": logo_url,
                    "order_id": order_id, 
                    "callback_url": payment_success_callback,
                    "prefill": {
                        "name": user.name,
                        "email": user.email,
                        "contact": user.phone_number
                    },
                    "notes": {
                        "address": "This payment is going to StickyShape.com"
                    },
                    "theme": {
                        "color": "#3399cc"
                    }
                }

    # socketio.emit('error', 'Something went wrong!')
    return None

@checkout_bp.route('/payment_callback', methods=['POST'])
def payment_callback():
    user = get_current_user()
    user.place_order()
    return redirect(url_for('home.orders'))

@checkout_bp.route( '/getShippingAddress' )
def getShippingAddress():
    user = get_current_user()
    data = {
        'address' : user.address    
    }

    return render_template('ui/shipping_address.html', data = data)

@checkout_bp.route( '/updateShippingAddress', methods=['POST'])
def updateShippingAddress():
    data = request.get_json()
    errors = []
    form_data = data.get('formData')

    recipient_name = form_data.get('recipient_name', "").strip()
    address_line1 = form_data.get('address_line1', "").strip()
    address_line2 = form_data.get('address_line2', "").strip()
    city = form_data.get('city', "").strip()
    state = form_data.get('state', "").strip()
    postal_code = form_data.get('postal_code', "").strip()
    country = form_data.get('country', "").strip()
    phone_number = form_data.get('phone_number', "").strip()

    if recipient_name == "":
        errors.append("Recipient Name is required.")
    if address_line1 == "":
        errors.append("Address is required.")
    if postal_code == "":
        errors.append("Postal Code is required.")
    try:
        int(postal_code)
    except ValueError:
        errors.append("Postal Code takes integer values only!")

    if city == "":
        errors.append("City is required.")
    if state == "":
        errors.append("State is required.")
    if country == "":
        errors.append("Country is required.")
    if phone_number == "":
        errors.append("Phone number is required")   

    try:
        int(phone_number)
    except ValueError:
        errors.append("Phone number takes integer values only!")


    if len(errors) > 0:
        response = {'status': 'error', 'errors': errors}
        # socketio.emit('error', errors[0])
        # raise Exception(str(response))
        return {'error': errors[0]}

    user = get_current_user()    
    user.add_or_update_address(recipient_name=recipient_name, addressLine1=address_line1, city=city, state=state, country=country, pincode=postal_code, addressLine2=address_line2, phone_number=phone_number, order_id=None)

    return {}

# csrf = CSRFProtect(app)
# csrf.exempt(checkout_bp)
app.register_blueprint(checkout_bp)