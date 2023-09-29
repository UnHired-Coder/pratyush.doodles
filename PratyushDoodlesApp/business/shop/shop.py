from flask import Flask, render_template, redirect, url_for, flash, Blueprint
from ... import app
from ...forms.AddItemForm import AddItemForm
from ...models.User.UserModel import User

shop_bp = Blueprint('shop', __name__)

# Define routes and views for the 'auth' Blueprint
@shop_bp.route('/shop')
def shop():
    return render_template('shop.html')

@shop_bp.route('/add_item', methods=['GET', 'POST'])
def add_item():
    form = AddItemForm()
    if form.validate_on_submit():
        # Create a new item and add it to the database
        user_id = 1  # Replace with the actual user ID
        item_name = form.item_name.data
        quantity = form.quantity.data
        item_description = form.item_description.data
        item_picture_urls = form.item_picture_urls.data.split(',')

        # Create and add the item to the database
        user = User.query.get(user_id)
        user.add_item_to_cart(item_name, quantity, item_description, item_picture_urls)

        flash('Item added to the cart!', 'success')
        return redirect(url_for('shop.add_item'))

    return render_template('add_item.html', form=form)

# @shop_bp.route('/cart_items')
# def cart_items():
#     user_id = 1  # Replace with the actual user ID
#     user = User.query.get(user_id)
#     cart_items = user.get_cart_items()
#     return render_template('cart_items.html', cart_items=cart_items)

app.register_blueprint(shop_bp)