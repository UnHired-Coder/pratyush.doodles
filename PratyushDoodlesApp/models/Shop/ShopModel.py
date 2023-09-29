from flask import Flask
from ... import db

class CartItem(db.Model):
    __tablename__ = 'cart_items'

    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(255), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    item_description = db.Column(db.Text, nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    # Define a one-to-many relationship between CartItem and ItemPicture
    pictures = db.relationship('ItemPicture', backref='cart_item', lazy=True)

    def __init__(self, item_name, quantity, item_description=None, user=None):
        self.item_name = item_name
        self.quantity = quantity
        self.item_description = item_description
        self.user = user  # Associate the cart item with a user

    def __repr__(self):
        return f'<CartItem {self.item_name}>'

class ItemPicture(db.Model):
    __tablename__ = 'item_pictures'

    id = db.Column(db.Integer, primary_key=True)
    picture_url = db.Column(db.String(255), nullable=False)
    cart_item_id = db.Column(db.Integer, db.ForeignKey('cart_items.id'), nullable=False)  # ForeignKey to CartItem

    def __init__(self, picture_url, item=None):
        self.picture_url = picture_url
        self.cart_item = cart_item  # Associate the picture with a cart item

    def __repr__(self):
        return f'<ItemPicture {self.picture_url}>'