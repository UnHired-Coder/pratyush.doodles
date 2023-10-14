from flask import render_template, Blueprint, jsonify, flash
from .. import app, razorpayClient
from .util import *
from .cart import getCartData
from ..forms.ShippingAddressForm import ShippingAddressForm
from .. import socketio


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

    recipient_name = data.form_data.get('recipient_name', '')
    address_line1 = data.form_data.get('address_line1', '')
    city = data.form_data.get('city', '')
    state = data.form_data.get('state', '')
    postal_code = data.form_data.get('postal_code', '')
    country = data.form_data.get('country', '')

    if not recipient_name:
        errors.append("Recipient Name is required.")
    if not address_line1:
        errors.append("Address Line 1 is required.")
    if not city:
        errors.append("City is required.")
    if not state:
        errors.append("State is required.")
    if not postal_code:
        errors.append("Postal Code is required.")
    if not country:
        errors.append("Country is required.")

    if errors:
        response = {'status': 'error', 'errors': errors}
    else:
        response = {'status': 'success'}



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