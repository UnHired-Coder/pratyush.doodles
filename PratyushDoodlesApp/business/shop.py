from flask import render_template, request, Blueprint #, Flask, redirect, url_for, flash
from .. import app
# from .. import app, socketio
# from ..forms.AddItemForm import ProductForm
# from ..models.UserModel import User
from .util import *
from ..models.ProductModel import Product, ProductImage
# from ..models.FaqModel import Faq
# from .. import db
from random import shuffle


shop_bp = Blueprint('shop', __name__)

# Define routes and views for the 'auth' Blueprint
@shop_bp.route('/', methods=['GET'])
@shop_bp.route('/shop', methods=['GET'])
@shop_bp.route('/shop/', methods=['GET'])
def shop():
    user = get_current_user()
    products = Product.query.all()
   
    # If it's a single product to show
    product_id = request.args.get('product_id')
    if product_id:
        is_admin = False
        if(user.email == "pratyushfree@gmail.com" and user.name == "Pratyush Tiwari"):
            is_admin = True

        product = Product.query.filter_by(id = product_id).first()
        suggested_products = Product.query.filter(Product.id != product_id and Product.product_category == product.product_category).limit(20).all()

        shuffle(suggested_products)
        suggested_products = suggested_products[:6]

        data = {
            'user': user,
            'product': product,
            'suggested_products': suggested_products,
            'is_admin': is_admin
        }

        return render_template('shop_product.html', data = data)

    product_categories = ['Cupid\'s Crew', 'Cat (Lity Fam)', 'Stickers',
                          # 'Movie Cards'
                          ]

    products_with_categories = {}

    for category in product_categories:
        product_in_this_category = Product.query.filter_by(product_category = category).all()
        shuffle(product_in_this_category)

        if(len(product_in_this_category) > 0):
            products_with_categories[category] = product_in_this_category

    data = {
        'user': user,
        'products_with_categories': products_with_categories
    }

    return render_template('shop.html', data = data)


@shop_bp.route('/get_products', methods=['GET'])
@shop_bp.route('/get_products/', methods=['GET'])
def get_products():
    user = get_current_user()

    # If it's a single product to show
    product_id = request.args.get('product_id')
    filters = request.args.getlist('filter_by')

    print("filter_by: "+str(len(filters)))

    if product_id:
        is_admin = False
        if(user.email == "pratyushfree@gmail.com" and user.name == "Pratyush Tiwari"):
            is_admin = True
        product = Product.query.filter_by(id = product_id).first()

        data = {
            'user': user,
            'product': product,
            'is_admin': is_admin
        }

        return render_template('shop_product.html', data = data)

    page_no = int(request.args.get('page') or 0)
    category = request.args.get('category')
    has_more_items = False

    start_id = max(0, page_no-1) * 6

    try:
        base_query = Product.query.filter_by(product_category=category).order_by(Product.id.desc()).offset(start_id)
        has_more_items = base_query.count() > 6
        product_in_this_category = base_query.limit(6).all()

        filtered_list = []
        if len(filters) == 0:
            filtered_list = product_in_this_category
        else:
            for product in product_in_this_category:
                if product.product_highlight in filters:
                    filtered_list.append(product)
        if len(filtered_list) != 0:
            shuffle(filtered_list)

    except Exception as e:
        filtered_list = []

    data = {
        'user': user,
        'products': filtered_list,
        'category': category,
    }

    return  {"products" :render_template('ui/products_list.html', data=data), "filters":filters, "has_more_items":has_more_items, "has_items": (len(filtered_list) > 0 or start_id > 0)}


#Admin actions
# @shop_bp.route('/add_product', methods=['GET', 'POST'])
# def add_product():
#     form = ProductForm()
#     print(form.validate())
#     if form.validate_on_submit():
#         product_name = form.name.data
#         product_description = form.description.data
#         product_price = form.price.data
#         product_stock_quantity = form.stock_quantity.data
#         discount_percent = form.discount_percent.data
#         product_highlight = form.product_highlight.data
#         product_category = form.product_category.data

#         # Get the list of image URLs
#         image_urls = [url for url in form.images.data.split(',')]

#         # Now you have the product data and the list of image URLs

#         # Redirect to a success page or perform further actions
#         product = Product(name = product_name, description = product_description, price = product_price, stock_quantity=product_stock_quantity, discount_percent = discount_percent, product_highlight= product_highlight, product_category = product_category)
#         db.session.add(product)
#         db.session.flush()

#         for image_url in image_urls:
#             image = ProductImage(picture_url = image_url, product_id = product.id)
#             db.session.add(image)
#             db.session.flush()

#         db.session.commit()    

#         print(image_urls)
#     else:
#         print(form.errors)

#         # images = ProductImage()
        

#     return render_template('add_item.html', form=form)

# @shop_bp.route('/add_faqs', methods=['GET', 'POST'])
# def add_afqs():

#     faq = Faq(question="How long will it take to receive my stickers?", answer="We dispatch your order within 2 business days, and delivery time varies based on your location. You can expect your stickers to arrive as per standard postal service timelines.")
#     db.session.add(faq)

#     faq = Faq(question="Do you provide tracking information for my order?", answer="Yes, we share tracking information via email once your order is dispatched. You can monitor the progress of your delivery.")
#     db.session.add(faq)

#     faq = Faq(question="Can I return or exchange my stickers?", answer="We apologize, but we do not accept returns or exchanges for stickers. All sales are final.")
#     db.session.add(faq)

#     faq = Faq(question="What if my stickers arrive damaged?", answer="We take great care in packaging your stickers to ensure they arrive in excellent condition. If, however, your stickers are damaged during transit, please contact us at stickyshapestore@gmail.com with a photo of the damaged items, and we'll assist you accordingly.")
#     db.session.add(faq)

#     faq = Faq(question="Can I get a refund for my purchase?", answer="We process refunds in cases of damaged or defective stickers. Please contact us at stickyshapestore@gmail.com with details and photos, and we'll initiate the refund process.")
#     db.session.add(faq)

#     faq = Faq(question="What kind of quality can I expect from your stickers?", answer="Our stickers are crafted with care on high-quality glossy paper. They are designed to be durable, vibrant, and long-lasting.")
#     db.session.add(faq)

#     db.session.commit()
#     data = {}
#     return render_template('questions.html', data=data)


app.register_blueprint(shop_bp)