from flask import Flask
from ... import db

class Product(db.Model):
    __tablename__ = 'product'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    stock_quantity = db.Column(db.Integer, nullable=False)

 
    # Relationships
    # 1:M
    product_images = db.relationship('ProductImages', backref = 'of_product', lazy=True)


    def __init__(self, name, description, price, stock_quantity, product_images):
        self.name = name
        self.product_id = description
        self.price = price
        self.stock_quantity = stock_quantity
        self.product_images = product_images


    def __repr__(self):
        return f'<Product {self.name}>'


class ProductImages(db.Model):
    __tablename__ = 'product_images'

    id = db.Column(db.Integer, primary_key=True)
    picture_url = db.Column(db.String(255), nullable=False)

    # Relationships
    # M:1
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

    def __init__(self, picture_url, product_id):
        self.picture_url = picture_url
        self.product_id = product_id

    def __repr__(self):
        return f'<ProductImages {self.picture_url}>'