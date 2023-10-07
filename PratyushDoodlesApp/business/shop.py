from flask import Flask, render_template, redirect, url_for, flash, Blueprint
from .. import app, socketio
from ..forms.AddItemForm import ProductForm
from ..models.UserModel import User
from .util import *
from ..models.ProductModel import Product, ProductImage
from .. import db

shop_bp = Blueprint('shop', __name__)

# Define routes and views for the 'auth' Blueprint
@shop_bp.route('/shop')
def shop():
    user = get_current_user()
    products = Product.query.all()

    data = {'user': user}
    if len(products) == 0:
        data['show_error'] = "No Products Listed!"
    else:
        data['products'] = products

    return render_template('shop.html', data = data)











#Admin actions
@shop_bp.route('/add_product', methods=['GET', 'POST'])
def add_product():
    form = ProductForm()
    print(form.validate())
    if form.validate_on_submit():
        product_name = form.name.data
        product_description = form.description.data
        product_price = form.price.data
        product_stock_quantity = form.stock_quantity.data

        # Get the list of image URLs
        image_urls = [url for url in form.images.data.split(',')]

        # Now you have the product data and the list of image URLs

        # Redirect to a success page or perform further actions
        product = Product(name = product_name, description = product_description, price = product_price, stock_quantity=product_stock_quantity)
        db.session.add(product)
        db.session.flush()

        for image_url in image_urls:
            image = ProductImage(picture_url = image_url, product_id = product.id)
            db.session.add(image)
            db.session.flush()

        db.session.commit()    

        print(image_urls)
    else:
        print(form.errors)

        # images = ProductImage()
        

    return render_template('add_item.html', form=form)
   

app.register_blueprint(shop_bp)