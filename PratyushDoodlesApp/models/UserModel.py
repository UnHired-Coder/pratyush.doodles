from flask import Flask
from .. import db
from ..models.ProductModel import Product
from datetime import datetime

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    mobile_number = db.Column(db.String(15), unique=True, nullable=True)
    email = db.Column(db.String(255), nullable=False)

    # Relationships
    # 1:1
    address = db.relationship('Address', backref = 'of_user', lazy=True)

    # 1:1
    cart = db.relationship('Cart', backref='of_user', lazy=True, uselist=False)

    # 1:M
    orders = db.relationship('Order', backref='of_user', lazy=True)

    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.initialize_cart()

    def initialize_cart(self):
        db.session.add(self)
        db.session.flush()
        self.cart = Cart(self.id)
        db.session.commit()

    def add_or_update_address(self):
        pass

    def place_order(self):
        self.cart.place_order()

    def cancel_order(self):
        pass            

    def get_formated_address(self):
        pass    

    def logout(self):
        pass    

    def __repr__(self):
        return f'<User {self.email}>'


class Cart(db.Model):
    __tablename__ = 'cart'
    
    id = db.Column(db.Integer, primary_key=True)
    creation_date = db.Column(db.Date, nullable=False)

    # Relationships
    # 1:M
    cart_items = db.relationship('CartItem', backref='of_cart', lazy=True)

    # 1:1
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


    def __init__(self, user_id):
        self.user_id = user_id
        self.creation_date = datetime.now().date()

    def add_to_cart(self, product_id):
        cart_item = CartItem.query.filter_by(product_id = product_id).first()
        if cart_item is None:
            cart_item = CartItem(cart_id = self.id, product_id = product_id)
        else :
            cart_item.update_quantity(delta = +1)
        db.session.add(cart_item)
        db.session.commit()

    def remove_from_cart(self, product_id):
        cart_item = CartItem.query.filter_by(product_id = product_id).first()
        db.session.delete(cart_item)
        db.session.commit()

    def place_order(self):
        order_items = []
        total_amount = 0
        for cartItem in self.cart_items:
            order_item = OrderItem(cart_id = self.id, product_id = cartItem.product_id, quantity = cartItem.quantity)
            order_items.append(order_item)
            product = Product.query.filter_by(id = cartItem.product_id).first()
            total_amount += product.price

        order = Order(user_id = self.id, address = self.address, order_items = order_items, amount = total_amount)

    def order_placed(self):
        pass    
        
    def __repr__(self):
        return f'<Cart {self.cart_items}>'


class CartItem(db.Model):
    __tablename__ = 'cart_item'

    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    

    # Relationships
    # M:1 
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'), nullable=False)
    
    # 1:1 
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)  

    def __init__(self, product_id, cart_id, quantity=1):
        self.product_id = product_id
        self.cart_id = cart_id
        self.quantity = quantity

    def update_quantity(self, delta):
        self.quantity += delta
        assert self.quantity >= 0

    def get_product(self):
        product = Product.query.filter_by(id = self.product_id).first()
        return product    

    def __repr__(self):
        return f'<CartItem {self.cart_id}>'


class Order(db.Model):
    __tablename__ = 'order'

    id = db.Column(db.Integer, primary_key=True)
    order_date = db.Column(db.Date, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(255), nullable=False)

    # Relationships
    # M:1
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # 1:1
    address = db.relationship('Address', backref = 'of_order', lazy=True)

    # 1:M 
    order_items = db.relationship('OrderItem', backref='of_order', lazy=True)


    def __init__(self, user_id, address, order_items, amount):
        self.user_id = user_id
        self.address = address
        self.order_items = order_items
        self.order_date = datetime.now().date()
        self.amount = amount
        self.status = "Dispatched"

    def cancel_order(self):
        pass    

    def __repr__(self):
        return f'<Order {self.order_date} {self.amount}>'


class OrderItem(db.Model):      
    __tablename__ = 'order_item'
    
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)

    # relationships
    # M:1
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)

    # 1:1 
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)


    def __init__(self, quantity, price, product_id):
        self.quantity = quantity
        self.price = price
        self.product_id = product_id

    def set_order_id(self, order_id):
        self.order_id = order_id   
    
    def __repr__(self):
        return f'<OrderItem {self.product_id}>'    


class Address(db.Model):
    __tablename__ = 'address'
    
    id = db.Column(db.Integer, primary_key=True)
    recipient_name = db.Column(db.String(255), nullable=False)

    addressLine1 = db.Column(db.String(255), nullable=False)
    addressLine2 = db.Column(db.String(255), nullable=True)
    street  = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(255), nullable=False)
    state = db.Column(db.String(255), nullable=False)
    pincode = db.Column(db.String(255), nullable=False)
    mobile_number = db.Column(db.String(15), nullable=False)


    # Relationships
    # M:1
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    # M:1
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=True)


    def __init__(self, recipient_name, addressLine1, street, city, state, pincode, addressLine2=None, user_id=None, order_id=None):
        self.recipient_name = recipient_name
        self.addressLine1 = addressLine1
        self.addressLine2 = addressLine2
        self.street = street
        self.city = city
        self.state = state
        self.pincode = pincode
        self.mobile_number = mobile_number

    def update_address(self):
        pass    

    def __repr__(self):
        return f'<Address {self.addressLine1}>'        