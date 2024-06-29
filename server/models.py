from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime
from sqlalchemy.ext.hybrid import hybrid_property


app = Flask(__name__)

db = SQLAlchemy()

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    
    serialize_rules = ('-cart.user', '-cart.id', '-cart.user_id', '-cart.product_id',)
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    contacts = db.Column(db.String)
    address = db.Column(db.String)
    
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    cart = db.relationship('Cart', back_populates = 'user')
    
    # products = db.relationship('Product', secondary='carts' , backref='user')
    # orders = db.relationship('Order',backref='user')

class Product(db.Model, SerializerMixin):
    __tablename__ = 'products'
    
    serialize_rules = ( '-images.product', '-images.img', '-cart.product')
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    category = db.Column(db.String)
    sub_category = db.Column(db.String)
    tag = db.Column(db.String)
    price = db.Column(db.Integer)
    quantity = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    
    images = db.relationship('Image', backref='product')
    cart = db.relationship('Cart', back_populates = 'product')

    # users = db.relationship('User', secondary='carts', backref='product')
    
    # images = re
    
class Image(db.Model, SerializerMixin):
    __tablename__ = 'images'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    img = db.Column(db.Text, nullable = False)
    name = db.Column(db.String, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)
    

class Cart(db.Model, SerializerMixin):
    __tablename__ = 'carts'

    serialize_rules = ( '-user.cart', '-product.cart', )

    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    
    
    user = db.relationship('User', back_populates = 'cart')
    product = db.relationship('Product', back_populates = 'cart')


    def __repr__(self):
        return f'(id={self.id}, product={self.product_id} user={self.user_id} quantity={self.quantity})'    
    

   
class Order(db.Model, SerializerMixin):
    __tablename__ = 'orders'

    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    overview = db.Column(db.String)

    
    # products = db.relationship('Product', secondary='orderproducts' , backref='order')
    
class OrderProduct(db.Model, SerializerMixin):
    
    __tablename__ = 'orderproducts'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    
    
    
    
    
    
    
    

