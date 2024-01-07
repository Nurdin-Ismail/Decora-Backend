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
    
api.add_resource(Users, '/users')
            










if __name__ == '__main__':
    app.run(port=5555)