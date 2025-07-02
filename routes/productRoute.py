from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from models import Product  # Ensure the Product model is imported

# Create blueprint for product routes
product_bp = Blueprint('product', __name__)

@product_bp.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([product.to_dict() for product in products]), 200

@product_bp.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    product = Product.query.get_or_404(id)
    return jsonify(product.to_dict()), 200

@product_bp.route('/products', methods=['POST'])
@jwt_required()  # Ensure only authenticated users can add products
def add_product():
    data = request.get_json()
    
    # Validate input data
    if not all(k in data for k in ('name', 'price', 'description', 'quantity')):
        return jsonify({'error': 'Missing data'}), 400
    
    # Create a new product instance
    new_product = Product(
        name=data['name'],
        price=data['price'],
        description=data['description'],
        quantity=data['quantity']  # Ensure you include quantity
    )
    
    # Add to the database session and commit
    db.session.add(new_product)
    db.session.commit()
    
    return jsonify(new_product.to_dict()), 201

@product_bp.route('/products/<int:id>', methods=['PUT'])
@jwt_required()
def update_product(id):
    product = Product.query.get_or_404(id)
    data = request.get_json()

    # Update product fields if provided
    if 'name' in data:
        product.name = data['name']
    if 'price' in data:
        product.price = data['price']
    if 'description' in data:
        product.description = data['description']
    if 'quantity' in data:
        product.quantity = data['quantity']  # Ensure quantity can also be updated

    db.session.commit()  # Commit changes to the database

    return jsonify(product.to_dict()), 200  # Return updated product

@product_bp.route('/products/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product deleted'}), 204
