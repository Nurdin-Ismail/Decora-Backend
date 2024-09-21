# Decora-Backend

# E-Commerce Flask RESTful API

## Overview
This is a RESTful API built with Flask for an e-commerce platform. The API allows for the management of products, users, carts, orders, and payment processing through M-Pesa. While the API is functional, it is currently not fully optimized for responsive design.

## Features
- CRUD operations for products, users, and carts
- User authentication and profile management
- Order management
- M-Pesa payment integration
- Image retrieval for products

## Technologies Used
- **Backend**: Flask
- **Database**: SQL (with SQLAlchemy)
- **Payment Integration**: M-Pesa

## API Endpoints

### 1. Root Endpoint
- **GET /**  
  Returns a welcome message.
  - **Response**: 
    - `200`: `"Hello"`

### 2. Products
- **GET /products**  
  Retrieve a list of all products.
  - **Response**: 
    - `200`: Array of products
- **GET /product/{id}**  
  Retrieve a single product by its ID.
  - **Parameters**: 
    - `id` (integer): The ID of the product
  - **Responses**:
    - `200`: Product details
    - `404`: Product not found

### 3. Images
- **GET /image/{id}**  
  Retrieve an image by its ID.
  - **Parameters**:
    - `id` (integer): The ID of the image
  - **Responses**:
    - `200`: Image in binary format
    - `404`: Image not found

### 4. Users
- **GET /users**  
  Retrieve a list of all users.
  - **Response**: 
    - `200`: Array of users
- **POST /users**  
  Create a new user.
  - **Request Body**: User details
  - **Response**: 
    - `200`: Created user details
- **GET /user/{id}**  
  Retrieve a single user by their ID.
  - **Parameters**: 
    - `id` (integer): The ID of the user
  - **Responses**:
    - `200`: User details
    - `404`: User not found
- **PATCH /user/{id}**  
  Update a user's details.
  - **Parameters**: 
    - `id` (integer): The ID of the user
  - **Request Body**: Updated user details
  - **Responses**:
    - `200`: Updated user details
    - `404`: User not found
- **DELETE /user/{id}**  
  Delete a user by their ID.
  - **Parameters**: 
    - `id` (integer): The ID of the user
  - **Responses**:
    - `200`: User deleted
    - `404`: User not found

### 5. Carts
- **GET /carts**  
  Retrieve a list of all carts.
  - **Response**: 
    - `200`: Array of carts
- **POST /carts**  
  Create a new cart.
  - **Request Body**: Cart details
  - **Response**: 
    - `200`: Created cart details
- **GET /cart/{id}**  
  Retrieve a cart by its ID.
  - **Parameters**: 
    - `id` (integer): The ID of the cart
  - **Responses**:
    - `200`: Cart details
    - `404`: Cart not found
- **PATCH /cart/{id}**  
  Update a cart's details.
  - **Parameters**: 
    - `id` (integer): The ID of the cart
  - **Request Body**: Updated cart details
  - **Responses**:
    - `200`: Updated cart details
    - `404`: Cart not found
- **DELETE /cart/{id}**  
  Delete a cart by its ID.
  - **Parameters**: 
    - `id` (integer): The ID of the cart
  - **Responses**:
    - `200`: Cart deleted
    - `404`: Cart not found

### 6. Orders
- **POST /orders**  
  Create a new order.
  - **Request Body**: Order details
  - **Response**: 
    - `200`: Created order details

### 7. M-Pesa Payment
- **POST /mpesa**  
  Initiate a payment using the M-Pesa API.
  - **Request Body**: 
    - `number` (string): Phone number
    - `amount` (integer): Payment amount
  - **Responses**:
    - `200`: Payment initiated
    - `500`: Failed to initiate payment

## License
This project is licensed under the MIT License. Feel free to use it for personal purposes, but please do not distribute it.
