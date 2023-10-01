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
    product_images = db.relationship('ProductImage', backref = 'of_product', lazy=True)


    def __init__(self, name, description, price, stock_quantity):
        self.name = name
        self.description = description
        self.price = price
        self.stock_quantity = stock_quantity


    def __repr__(self):
        return f'<Product {self.name}>'


class ProductImage(db.Model):
    __tablename__ = 'product_image'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), nullable=False)

    # Relationships
    # M:1
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

    def __init__(self, url, product_id):
        self.url = url
        self.product_id = product_id

    def __repr__(self):
        return f'<ProductImage {self.url}>'