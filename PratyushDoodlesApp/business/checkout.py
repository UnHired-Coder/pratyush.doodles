from flask import render_template, Blueprint, jsonify, flash, redirect, url_for
from .. import app, razorpayClient
from .util import *
from .cart import getCartData
from ..forms.ShippingAddressForm import ShippingAddressForm
from .. import socketio
from ..models.UserModel import Address
from .. import db

checkout_bp = Blueprint('checkout', __name__)

# Define routes and views for the 'auth' Blueprint
@checkout_bp.route('/checkout')
def checkout():
    data = getCartData()
    return render_template('checkout.html', data=data)

@checkout_bp.route('/initiate_payment', methods=['GET', 'POST'])
def initiate_payment():
    amount = 1000  # The amount to be paid in paise (e.g., 1000 paise = ₹10)
    currency = 'INR'  # Currency code (e.g., INR for Indian Rupees)

    payment_data = {
        'amount': amount,
        'currency': currency,
    }

    # Create a Razorpay order
    order = razorpayClient.order.create(payment_data)

    # Return the order ID to the client-side for payment initiation
    return jsonify({'order_id': order['id']})

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


# @socketio.on( '' )
# def shipping_address():
#     form = ShippingAddressForm()

#     if form.validate_on_submit():
#         # Process the form data (e.g., save it to a database)
#         # For this example, we'll just print the data to the console
#         print(f'Recipient Name: {form.recipient_name.data}')
#         print(f'Address Line 1: {form.address_line1.data}')
#         print(f'Address Line 2: {form.address_line2.data}')
#         print(f'City: {form.city.data}')
#         print(f'State: {form.state.data}')
#         print(f'Postal Code: {form.postal_code.data}')
#         print(f'Country: {form.country.data}')

#         # Redirect to a success page or do something else
#         return redirect(url_for('success'))

#     # If the form is not valid, show error messages
#     for field, errors in form.errors.items():
#         for error in errors:
#             flash(f"Error in field '{field}': {error}")

#     return render_template('shipping_address.html', form=form)

app.register_blueprint(checkout_bp)