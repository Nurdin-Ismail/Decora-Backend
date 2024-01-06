#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response, Response
from flask_migrate import Migrate
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS
from sqlalchemy import desc, asc



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
            imeji = Image.query.filter(Image.product_id == product.id).all()
            for img in imeji:
                imeji_list.append('/image/' + str(img.id))
            product_dict = {
                "id": product.id,
                "name" : product.name,
                "description" :product.description,
                "category" : product.category,
                "sub_category" : product.sub_category,
                "tag" : product.tag,
                "price" : product.price,
                "quantity" : product.quantity,
                "images" : imeji_list
                
            }
            
            list.append(product_dict)
            
        return make_response(jsonify(list), 200)
api.add_resource(Products, '/products')
            


class Imagebyid(Resource):
    def get(self, id):
        image = Image.query.filter(Image.id == id).first()
        if image:
            return Response(image.img, mimetype=image.mimetype)
        
api.add_resource(Imagebyid, '/image/<int:id>')










if __name__ == '__main__':
    app.run(port=5555)