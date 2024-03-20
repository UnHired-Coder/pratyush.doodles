from flask import render_template
from flask import Blueprint, request
from .. import app
from ..models.UserModel import Order
from ..models.FaqModel import Faq
from .util import *
from ..forms.AddItemForm import ProductForm, DeleteProductForm
from ..models.ProductModel import Product, ProductImage


others_bp = Blueprint('others', __name__)
# Define routes and views for the 'auth' Blueprint
@others_bp.route('/questions', methods=['GET'])
@others_bp.route('/questions/', methods=['GET'])
def questions():
    user = get_current_user()
    data = {
            'user': user
    }
  
    return render_template('questions.html', data=data)

@others_bp.route('/getFaqs', methods=['GET'])
@others_bp.route('/getFaqs/', methods=['GET'])
def getFaqs():
    # Fetch cart items as a list of objects
    faqs = Faq.query.all()
    data = {
        'faqs' : faqs
    }

    # Render the Jinja2 template with the cart items
    rendered_template = render_template('ui/faq_item.html', data=data)
    return rendered_template


@others_bp.route('/contact', methods=['GET'])
@others_bp.route('/contact/', methods=['GET'])
def contact():
    user = get_current_user()
    data = {
            'user': user
    }

    return render_template('contact.html', data=data)

@others_bp.route('/about', methods=['GET'])
@others_bp.route('/about/', methods=['GET'])
def about():
    user = get_current_user()
    data = {
            'user': user
    }

    return render_template('about.html', data=data)

@others_bp.route('/privacypolicy', methods=['GET'])
@others_bp.route('/privacypolicy/', methods=['GET'])
def privacypolicy():
    user = get_current_user()
    data = {
            'user': user
    }

    return render_template('policies/privacypolicy.html', data=data)    


@others_bp.route('/termsandconditions', methods=['GET'])
@others_bp.route('/termsandconditions/', methods=['GET'])
def termsandconditions():
    user = get_current_user()
    data = {
            'user': user
    }

    return render_template('policies/termsandconditions.html', data=data)    


@others_bp.route('/cancellationpolicy', methods=['GET'])
@others_bp.route('/cancellationpolicy/', methods=['GET'])
def cancellationpolicy():
    user = get_current_user()
    data = {
            'user': user
    }

    return render_template('policies/cancellationpolicy.html', data=data)    


@others_bp.route('/pricing', methods=['GET'])
@others_bp.route('/pricing/', methods=['GET'])
def pricing():
    return render_template('policies/pricing.html')    



@others_bp.route('/admin/3fiMeTqc2v', methods=['GET'])
@others_bp.route('/admin/3fiMeTqc2v/', methods=['GET'])
def admin():
    user = get_current_user()
    if(user.email != "pratyushfree@gmail.com" or user.name != "Pratyush Tiwari"):
        return ""

    from ..models.UserModel import User, Order, OrderItem
    from ..models.ProductModel import Product

    orders =  Order.query.all()
    number_of_orders = len(orders)

    all_orders = {}
    all_orders['order'] = []
    for order in orders:
        order_details = {}
        order_details['id'] = order.id
        order_details['order_date'] = order.order_date
        order_details['amount'] = order.amount
        order_details['status'] = order.status
        order_details['address'] = order.address

        order_details['order_item_details'] = []
        for order_item in order.order_items:
            product = Product.query.filter_by(id = order_item.product_id).first()
            order_item_details = {}
            order_item_details['product_id'] = product.id 
            order_item_details['name'] = product.name 
            order_item_details['price'] = product.price
            order_item_details['product_image'] = product.product_images[0].picture_url 

            order_details['order_item_details'] += [order_item_details]

        all_orders['order'] +=  [order_details]      

    data = {
        'number_of_orders' : number_of_orders,
        'all_orders': all_orders
    }



    new_orders = {}
    new_orders['order'] = []
    new_orders_ = Order.query.filter_by(status = "Order Placed").all()
    print(new_orders_)

    for order in new_orders_:
        order_details = {}
        order_details['id'] = order.id
        order_details['order_date'] = order.order_date
        order_details['amount'] = order.amount
        order_details['status'] = order.status
        order_details['address'] = order.address

        order_details['order_item_details'] = []
        for order_item in order.order_items:
            product = Product.query.filter_by(id = order_item.product_id).first()
            order_item_details = {}
            order_item_details['product_id'] = product.id 
            order_item_details['name'] = product.name 
            order_item_details['price'] = product.price
            order_item_details['product_image'] = product.product_images[0].picture_url 

            order_details['order_item_details'] += [order_item_details]

    new_orders['order'] +=  [order_details] 

    data['new_orders'] = new_orders

    users = User.query.filter(User.email != "guest@guest.com").all()
    data['users'] = users

    return render_template("adminActions/admin.html", data= data)


@others_bp.route('/admin/3fiMeTqc2v/add_product', methods=['POST', 'GET'])
@others_bp.route('/admin/3fiMeTqc2v//add_product/', methods=['POST', 'GET'])
def add_product():
    user = get_current_user()
    if(user.email != "pratyushfree@gmail.com" or user.name != "Pratyush Tiwari"):
        return ""    

    form = request.form

    if form:
        product_name = form['name']
        product_description = form['description']
        product_price = form['price']
        product_stock_quantity = form['stock_quantity']
        discount_percent = form['discount_percent']
        product_highlight = form['product_highlight']
        product_category = form['product_category']

        # Get the list of image URLs
        image_urls = [url for url in form['images'].split(',')]

        # Now you have the product data and the list of image URLs

        # Redirect to a success page or perform further actions
        product = Product(name = product_name, description = product_description, price = product_price, stock_quantity=product_stock_quantity, discount_percent = discount_percent, product_highlight= product_highlight, product_category = product_category)
        db.session.add(product)
        db.session.flush()

        for image_url in image_urls:
            image = ProductImage(picture_url = image_url, product_id = product.id)
            db.session.add(image)
            db.session.flush()

        db.session.commit()    

        print(image_urls) 
    form = ProductForm()
    return render_template('adminActions/add_product.html', form=form)




@others_bp.route('/admin/3fiMeTqc2v/delete_product', methods=['POST', 'GET'])
@others_bp.route('/admin/3fiMeTqc2v/delete_product/', methods=['POST', 'GET'])
def delete_product_with_id():
    user = get_current_user()
    if(user.email != "pratyushfree@gmail.com" or user.name != "Pratyush Tiwari"):
        return ""    

    form = request.form

    if form:
        product_id = form['delete_product_id']
        if product_id:
            product = Product.query.filter_by(id = product_id).delete()
            db.session.commit()

    form = DeleteProductForm()
    return render_template('adminActions/delete_product.html', form = form)


@others_bp.route('/update_status', methods=['POST'])
@others_bp.route('/update_status/', methods=['POST'])
def update_status():
    user = get_current_user()
    if(user.email != "pratyushfree@gmail.com" or user.name != "Pratyush Tiwari"):
        return ""

    import json

    data = request.get_json()
    status = data.get('data')
    order_id = data.get('order_id')
    
    print(status)
    print(order_id)

    order = Order.query.filter_by(id = order_id).first()
    order.status = status
    db.session.commit()
    return ""


app.register_blueprint(others_bp)