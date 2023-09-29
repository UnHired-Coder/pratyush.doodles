from flask import Flask
from ... import db
from ..Shop.ShopModel import CartItem, ItemPicture

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    mobile_number = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(255), nullable=True)
    address = db.Column(db.String(255), nullable=True)

    # Define a one-to-many relationship between User and CartItem
    cart_items = db.relationship('CartItem', backref='to_user', lazy=True)

    def __init__(self, name, mobile_number, address=None, email=None):
        self.name = name
        self.mobile_number = mobile_number
        self.address = address
        self.email = email

    def __repr__(self):
        return f'<User {self.name}>'

    def add_item_to_cart(self, item_name, quantity, item_description=None, item_picture_urls=None):
        # Create a new cart item and associate it with the user
        cart_item = CartItem(item_name=item_name, quantity=quantity, item_description=item_description, user=self)

        # Associate item pictures with the cart item
        if item_picture_urls:
            for picture_url in item_picture_urls:
                item_picture = ItemPicture(picture_url=picture_url, cart_item=cart_item)
                db.session.add(item_picture)

        db.session.add(cart_item)
        db.session.commit()

    def get_cart_items(self):
        # Retrieve and return all cart items associated with the user
        return self.cart_items