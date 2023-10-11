from flask import render_template, Blueprint, jsonify
from .. import app, razorpayClient
from .util import *
from .cart import getCartData


checkout_bp = Blueprint('checkout', __name__)

# Define routes and views for the 'auth' Blueprint
@checkout_bp.route('/checkout')
def checkout():
    user = get_current_user()
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


app.register_blueprint(checkout_bp)