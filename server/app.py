#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response, Response
from flask_migrate import Migrate
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS
from sqlalchemy import desc, asc
import requests
import json
from datetime import datetime
import base64





from models import *

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)
api = Api(app)
CORS(app)

MPESA_CONSUMER_KEY='gLUMAaJWogwRnMRHFOGLapbxBzMqSvGeX8I2zXyj1Oz8aFzG'
MPESA_CONSUMER_SECRET='64bEDtL7A3YLGIzeIYw5uJAJSiCdE9Gf9OtnBE9I3HeclvvZWoikR7PAkG7SGDE8'
MPESA_SHORTCODE=174379
MPESA_PASSKEY='bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'

def get_access_token():
    url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    auth = (MPESA_CONSUMER_KEY, MPESA_CONSUMER_SECRET)
    response = requests.get(url, auth=auth)
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        return None

@app.route('/')
def home():
    return make_response('Hello', 200)


class Products(Resource):
    def get(self):
        list = []
        for product in Product.query.all():
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
                "images" : image_list,
                "created_at" : product.created_at,
                "updated_at" : product.updated_at
                
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
            
            
            address = 'No address'
            if user.address != None:
                address = json.loads(user.address)
            else:
                address = 'No Address'

                
                
            user_dict= user.to_dict()

            if len(user_dict['cart']) > 0:
                # print(user_dict['cart'])

                for i in user_dict['cart']:
                    imageso = []

                    for k in i['product']['images']:
                        imeji = '/image/' + str(k['id'])

                        imageso.append(imeji)

                    i['product']['images'] = imageso

                    
                    

                     
                         



            
            users.append(user_dict)
            
        return make_response(jsonify(users), 200)
    
    def post(self):
        data = request.get_json()
        new_user = User(
            username = data.get('username'),
            email = data.get('email'),
            
            created_at = data.get('created_at'),
            password = data.get('password')
        )
        db.session.add(new_user)
        db.session.commit()
        
        new_user_dict = {
            "id": new_user.id,
            "username": new_user.username,
            "email": new_user.email,
            
            "created_at": new_user.created_at,
            "password": new_user.password
        }
        return make_response(jsonify(new_user_dict), 200)
        
    
api.add_resource(Users, '/users')

class UserById(Resource):
    
    def get(self, id):
        user = User.query.filter(User.id == id).first()

        
        if user:
            

            address = 'No address'
            if user.address != None:
                address = json.loads(user.address)
            else:
                address = 'No Address'



            user_dict= user.to_dict()

            if len(user_dict['cart']) > 0:
                # print(user_dict['cart'])

                for i in user_dict['cart']:
                    imageso = []

                    for k in i['product']['images']:
                        imeji = '/image/' + str(k['id'])

                        imageso.append(imeji)

                    i['product']['images'] = imageso
            
            
            return make_response(jsonify(user_dict), 200)
        else:
            return make_response(jsonify({"error": "User not found"}), 404)
        

    def patch(self, id):
        record = User.query.filter(User.id == id).first()
        if not record:
            return make_response({"error": "Record not found"}, 404)

        else:
            if request.content_type == 'application/json':

                
                data = request.json  # Get JSON data from the request body
                if data:
                    for key, value in data.items():
                        setattr(record, key, value)
                    db.session.add(record)
                    db.session.commit()
                    response_dict = {
                        "id": record.id,
                        "email": record.email,
                        "password": record.password,
                        "username": record.username
                    }

                    response = make_response(
                        jsonify(response_dict),
                        200
                    )

                    return response


                else:
                    return make_response({"error": "No data provided in JSON format"}, 400)

            else:
                for attr in request.form:
                    setattr(record, attr, request.form[attr])
                db.session.add(record)
                db.session.commit()

                response_dict = {
                        "id": record.id,
                        "email": record.email,
                        "password": record.password,
                        "username": record.username
                    }

                response = make_response(
                        jsonify(response_dict),
                        200
                    )

                return response

           

            

       
        
        
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
    
    def get(self):
        carts = []
        
        for cart in Cart.query.all():
            
            cart_dict = {
                "product_id": cart.product_id,
                         
                         }
            
            carts.append(cart_dict)
            
        
        return make_response(jsonify(carts), 200)   
    
    def post(self):
        data = request.get_json()
        
        
        new_cart= Cart(
            user_id = data.get('user_id'),
            product_id = data.get('product_id'),
            quantity = data.get('quantity')
        )
        db.session.add(new_cart)
        db.session.commit()
        
        new_cart_dict = {
            'user_id': new_cart.user_id,
            'product_id': new_cart.product_id
        }
        return make_response(jsonify(new_cart_dict), 200)
    
    
        
api.add_resource(Carts, '/carts')

class CartById(Resource):
    
    def get(self, id):
        cart = Cart.query.filter(Cart.id == id).first()

        
        if cart:
            # products = []
            # list = Cart.query.filter(user.id == Cart.user_id).all()
            # for item in list:
            #     res = requests.get(f'http://127.0.0.1:5555/product/{item.product_id}')
            #     response = json.loads(res.text)
            #     cart.append(response)

            cart_dict= {
                "id" : cart.id,
                "user_id" : cart.user_id,
                "product_id" : cart.product_id,
                "quantity" : cart.quantity
                
                
            }
            
            
            return make_response(jsonify(cart_dict), 200)
        else:
            return make_response(jsonify({"error": "Cart not found"}), 404)
        
    def patch(self,id):
        

        record = Cart.query.filter(Cart.id == id).first()
        if not record:
            return make_response({"error": "Record not found"}, 404)

        try:
            if request.content_type == 'application/json':

                
                data = request.json  # Get JSON data from the request body
                if data:
                    for key, value in data.items():
                        setattr(record, key, value)
                    db.session.add(record)
                    db.session.commit()
                else:
                    return make_response({"error": "No data provided in JSON format"}, 400)

            else:
                for attr in request.form:
                    setattr(record, attr, request.form[attr])
                db.session.add(record)
                db.session.commit()

           

            response_dict = {
                "id": record.id,
                "product_id": record.product_id,
                "quantity": record.quantity,
                "user_id": record.user_id
            }

            response = make_response(
                jsonify(response_dict),
                200
            )

            return response

        except Exception as e:
            return make_response({"error": str(e)}, 400)
        
    def delete(self, id):

        record = Cart.query.filter(Cart.id == id).first()

        db.session.delete(record)
        db.session.commit()

        response_dict = {"message": "record successfully deleted"}

        response = make_response(
            response_dict,
            200
        )

        return response

api.add_resource(CartById, '/cart/<int:id>')

class Orders(Resource):
    def post(self):
        data = request.get_json()
        
        
        new_order= Order(
            user_id = data.get('user_id'),
            overview = data.get('overview')
        )
        db.session.add(new_order)
        db.session.commit()
        
        new_order_dict = {
            'user_id': new_order.user_id,
            'Overview': new_order.overview
        }
        return make_response(jsonify(new_order_dict), 200)

api.add_resource(Orders, '/orders')


class MpesaPayment(Resource):
    def post(self):
        data = request.get_json()
        phone = data['number']
        amount = data['amount']
        access_token = get_access_token()
        print(access_token)

        if not access_token:
            return {'error': 'Could not get access token'}, 500

        url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        password = base64.b64encode(f'{MPESA_SHORTCODE}{MPESA_PASSKEY}{timestamp}'.encode('utf-8')).decode('utf-8')

        payload = {
            'BusinessShortCode': 174379,
            'Password': password,
            'Timestamp': timestamp,
            'TransactionType': 'CustomerPayBillOnline',
            'Amount': 1,
            'PartyA': phone,
            'PartyB': 174379,
            'PhoneNumber': phone,
            'CallBackURL': 'https://mydomain.com/path',
            'AccountReference': 'Test123',
            'TransactionDesc': 'Payment for goods'
        }

        response = requests.post(url, json=payload, headers=headers)
        print(f'Status Code: {response.status_code}')
        print(f'Response Content: {response.content.decode("utf-8")}')
        if response.status_code == 200:
            return response.json()
        else:

             return  response.status_code

api.add_resource(MpesaPayment, '/mpesa')






          










if __name__ == '__main__':
    app.run(port=5000)