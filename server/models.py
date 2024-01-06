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
    
    
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    contacts = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    

class Product(db.Model, SerializerMixin):
    __tablename__ = 'products'
    
    
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    category = db.Column(db.String)
    sub_category = db.Column(db.String)
    tag = db.Column(db.String)
    price = db.Column(db.Integer)
    quantity = db.Column(db.String)
    
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
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
        
    
    
    

    
    
    
    
    
    

