from flask import Flask
from .. import db
from ..models.ProductModel import Product
from datetime import datetime
from flask_login import UserMixin, LoginManager
from ..business.constants import SHIPPING_CHARGES

class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(15), unique=True, nullable=True)
    email = db.Column(db.String(255), nullable=False)


    # Relationships
    # 1:1
    address = db.relationship('Address', backref = 'of_user', lazy=True, uselist=False)

    # 1:1
    cart = db.relationship('Cart', backref='of_user', lazy=True, uselist=False)

    # 1:M
    orders = db.relationship('Order', backref='of_user', lazy=True)

    def __init__(self, name, email, guest_user=False):
        self.name = name
        self.email = email
        self.initialize_cart()

    def initialize_cart(self):
        db.session.add(self)
        db.session.flush()
        self.cart = Cart(self.id)
        db.session.commit()

    def merge_with_guest_user(self, guest_user):

        if guest_user.phone_number:
            self.phone_number = guest_user.phone_number
            guest_user.phone_number = -1 * guest_user.phone_number

        #Guest user address is now my address
        if guest_user.address:
            guest_user.address.user_id = self.id

        #Guest user cart is now my cart
        if guest_user.cart:
            for cart_item in guest_user.cart.cart_items:
                cart_item.cart_id = self.cart.id
            # Remove Guest User's cart
            Cart.query.filter_by(id=guest_user.cart.id).delete()    

        # Remove Guest User
        User.query.filter_by(id=guest_user.id).delete()    

        #Guest user orders are now my orders
        for order in guest_user.orders:
            order.user_id = self.id

        db.session.commit()

    def add_or_update_address(self, recipient_name, addressLine1, city, state, country, pincode, phone_number, order_id=None, addressLine2=None):
        address = Address.query.filter_by(user_id = self.id).first()
        updated_address = Address(recipient_name=recipient_name, addressLine1=addressLine1, city=city, state=state, country=country, pincode=pincode, addressLine2=addressLine2, phone_number=phone_number, user_id=self.id, order_id=None)

        if address:
            address.recipient_name = updated_address.recipient_name
            address.addressLine1 = updated_address.addressLine1
            address.city = updated_address.city
            address.state = updated_address.state
            address.country = updated_address.country
            address.pincode = updated_address.pincode
            address.addressLine2 = updated_address.addressLine2
            address.phone_number = updated_address.phone_number
            address.user_id = updated_address.user_id
            address.order_id = updated_address.order_id
        else:
            db.session.add(updated_address)

        self.address = updated_address
        self.phone_number = updated_address.phone_number
        db.session.commit()

    def place_order(self):
        self.cart.place_order()

    def ger_orders(self):
        return self.orders    

    def cancel_order(self):
        pass            

    def get_formated_address(self):
        pass    

    def logout(self):
        pass    

    @property
    def count_items_in_cart(self):
        count = 0
        for item in self.cart.cart_items:
            count += item.quantity
        return count

    @property
    def is_authenticated(self):
        # Return True if the user is authenticated, False otherwise
        if(self.email == 'guest@guest.com'):
            return False
        return True  # You can implement your own logic here

    @property
    def is_active(self):
        # Return True if the user is active, False otherwise
        return True  # You can implement your own logic here

    @property
    def is_anonymous(self):
        # Return True if the user is anonymous, False otherwise
        if(self.email == None):
            return True
        return False

    def get_id(self):
        # Return a unique identifier for the user
        return str(self.id)


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
        cart_item = CartItem.query.filter_by(cart_id = self.id, product_id = product_id).first()
        if cart_item is None:
            cart_item = CartItem(cart_id = self.id, product_id = product_id)
            db.session.add(cart_item)
        else :
            cart_item.update_quantity(delta = +1)    
       
        db.session.commit()

    def reduce_from_cart(self, product_id):
        cart_item = CartItem.query.filter_by(cart_id = self.id, product_id = product_id).first()

        if cart_item.quantity == 1:
            self.remove_from_cart(product_id)
        elif cart_item:
            cart_item.update_quantity(delta = -1) 

        db.session.commit()


    def remove_from_cart(self, product_id):
        cart_item = CartItem.query.filter_by(cart_id = self.id, product_id = product_id).first()
        db.session.delete(cart_item)
        db.session.commit()

    def place_order(self):
        order_items = []
        total_amount = 0
        for cartItem in self.cart_items:
            product = Product.query.filter_by(id = cartItem.product_id).first()
            total_amount += (product.price * cartItem.quantity)
            order_item = OrderItem(product_id = cartItem.product_id, quantity = cartItem.quantity, price =  product.price)
            order_items.append(order_item)
            db.session.delete(cartItem)
        
        order_address = self.of_user.address.copy()
        db.session.add(order_address)
        
        order = Order(user_id = self.user_id, address = order_address, order_items = order_items, amount = total_amount +  (0 if(len(order_items) >= 5) else SHIPPING_CHARGES))
        db.session.add(order)
        db.session.flush()

        order.address.order_id = order.id

        db.session.commit()

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
    # 1:1
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # 1:1
    address = db.relationship('Address', backref='of_order', lazy=True, uselist=False)

    # 1:M 
    order_items = db.relationship('OrderItem', backref='of_order', lazy=True)


    def __init__(self, user_id, address, order_items, amount):
        self.user_id = user_id
        self.address = address
        self.order_items = order_items
        self.order_date = datetime.now().date()
        self.amount = amount
        self.status = "Order Placed"

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
    city = db.Column(db.String(255), nullable=False)
    state = db.Column(db.String(255), nullable=False)
    pincode = db.Column(db.String(255), nullable=False)
    country = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)


    # Relationships
    # M:1
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    # M:1
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=True)


    def __init__(self, recipient_name, addressLine1, city, state, country, pincode, phone_number, user_id, order_id=None, addressLine2=None):
        self.recipient_name = recipient_name
        self.addressLine1 = addressLine1
        self.addressLine2 = addressLine2
        self.city = city
        self.state = state
        self.country = country
        self.pincode = pincode
        self.phone_number = phone_number
        self.user_id = user_id

    def copy(self):
        return Address(recipient_name=self.recipient_name, addressLine1=self.addressLine1, city=self.city, state=self.state, country=self.country, pincode=self.pincode, addressLine2=self.addressLine2, phone_number=self.phone_number, user_id=None, order_id=None)

    def update_address(self):
        pass    

    def __repr__(self):
        return f'{self.addressLine1}, {self.city}, {self.state}, {self.country}, {self.pincode}, \n Contact: {self.phone_number}'     