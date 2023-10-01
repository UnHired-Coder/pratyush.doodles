from flask import Flask, render_template, redirect, url_for, flash, Blueprint
from .. import app
from ..forms.AddItemForm import AddItemForm
from ..models.UserModel import User
from .util import *
from ..models.ProductModel import Product
from .. import db

shop_bp = Blueprint('shop', __name__)

# Define routes and views for the 'auth' Blueprint
@shop_bp.route('/shop')
def shop():
    products = Product.query.all()

    data = {
        'user': get_current_user(),
        'products': products
    }

    return render_template('shop.html', data = data)

app.register_blueprint(shop_bp)