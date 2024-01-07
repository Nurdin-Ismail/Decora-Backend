#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response, Response
from flask_migrate import Migrate
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS
from sqlalchemy import desc, asc
import requests
import json



from models import *

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)
api = Api(app)
CORS(app)

@app.route('/')
def home():
    return make_response('Hello', 200)


class Products(Resource):
    def get(self):
        list = []
        for product in Product.query.all():
            imeji_list = []
            image = Image.query.filter(Image.product_id == product.id).first()
             
            imeji = '/image/' + str(image.id)
            product_dict = {
                "id": product.id,
                "name" : product.name,
                "description" :product.description,
                "category" : product.category,
                "sub_category" : product.sub_category,
                "tag" : product.tag,
                "price" : product.price,
                "quantity" : product.quantity,
                "image" : imeji
                
            }
            
            list.append(product_dict)
            
        return make_response(jsonify(list), 200)
api.add_resource(Products, '/products')

class ProductById(Resource):
    def get(self, id):
        product = Product.query.filter(Product.id == id).first()
        
        if product:
            
            image_list = []
            images = Image.query.filter(Image.product_id == product.id).all()
            
            for img in images:
                imeji = '/image/' + str(img.id)
                
                image_list.append(imeji)
                
                
            
            product_dict = {
                "id": product.id,
                "name" : product.name,
                "description" :product.description,
                "category" : product.category,
                "sub_category" : product.sub_category,
                "tag" : product.tag,
                "price" : product.price,
                "quantity" : product.quantity,
                "images" : image_list
                
            }
            
            return make_response(jsonify(product_dict), 200)
        else:
            
            return make_response((jsonify({"error": "Product not found"}), 404))
        
api.add_resource(ProductById, '/product/<int:id>')           
            
            
            


class Imagebyid(Resource):
    def get(self, id):
        image = Image.query.filter(Image.id == id).first()
        if image:
            return Response(image.img, mimetype=image.mimetype)
        
api.add_resource(Imagebyid, '/image/<int:id>')

class Users(Resource):
    def get(self):
        users = []
        for user in User.query.all():
            cart = []
            list = Cart.query.filter(user.id == Cart.user_id).all()
            for item in list:
                res = requests.get(f'http://127.0.0.1:5555/product/{item.product_id}')
                response = json.loads(res.text)
                cart.append(response)
                
            user_dict= {
                "id" : user.id,
                "name" : user.username,
                "email" : user.email,
                "passord": user.password,
                "created_at" : user.created_at,
                "updated_at" : user.updated_at,
                "cart" : cart
                
            }
            
            users.append(user_dict)
            
        return make_response(jsonify(users), 200)
    
    def post(self):
        data = request.get_json()
        new_user = User(
            username = data.get('username'),
            email = data.get('email'),
            contacts = data.get('contacts'),
            created_at = data.get('created_at'),
            password = data.get('password')
        )
        db.session.add(new_user)
        db.session.commit()
        
        new_user_dict = {
            "id": new_user.id,
            "username": new_user.username,
            "email": new_user.email,
            "contacts": new_user.contacts,
            "created_at": new_user.created_at,
            "password": new_user.password
        }
        return make_response(jsonify(new_user_dict), 200)
        
    
api.add_resource(Users, '/users')

class UserById(Resource):
    
    def get(self, id):
        user = User.query.filter(User.id == id).first()
        
        if user:
            user_dict =user.to_dict()
            
            return make_response(jsonify(user_dict), 200)
        else:
            return make_response(jsonify({"error": "User not found"}), 404)
        
        
    def delete(self, id):
        user = User.query.filter(User.id == id).first()
        
        if user:
            db.session.delete(user)
            db.session.commit()
            
            return make_response(jsonify({"message": "User deleted successfully"}), 200)
        else:
            return make_response(jsonify({"error": "User not found"}), 404)

api.add_resource(UserById, '/user/<int:id>')

class Carts(Resource):
    
    def post(self):
        data = request.get_json()
        
        
        new_cart= Cart(
            user_id = data.get('user_id'),
            product_id = data.get('product_id')
        )
        db.session.add(new_cart)
        db.session.commit()
        
        new_cart_dict = {
            'user_id': new_cart.user_id,
            'product_id': new_cart.product_id
        }
        return make_response(jsonify(new_cart_dict), 200)
        
api.add_resource(Carts, '/carts')


          










if __name__ == '__main__':
    app.run(port=5550)