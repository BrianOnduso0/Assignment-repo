from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from models import Cart  # Make sure to import the Cart model

# Create blueprint for cart routes
cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/cart', methods=['POST'])
@jwt_required()
def add_to_cart():
    user_id = get_jwt_identity()  # Get the current user's identity from the JWT
    data = request.get_json()

    # Validate input data
    if 'product_id' not in data or 'quantity' not in data:
        return jsonify({'error': 'Missing product_id or quantity'}), 400

    # Create a new cart item
    cart_item = Cart(user_id=user_id, product_id=data['product_id'], quantity=data['quantity'])
    db.session.add(cart_item)
    db.session.commit()
    
    return jsonify({"message": "Added to cart"}), 201

@cart_bp.route('/cart', methods=['GET'])
@jwt_required()
def get_cart():
    user_id = get_jwt_identity()  # Get the current user's identity from the JWT
    items = Cart.query.filter_by(user_id=user_id).all()

    # Serialize each item in the cart
    return jsonify([item.to_dict() for item in items]), 200
