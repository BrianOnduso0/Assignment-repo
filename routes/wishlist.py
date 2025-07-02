from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from models import Wishlist  # Make sure to import the Wishlist model

# Create blueprint for wishlist routes
wishlist_bp = Blueprint('wishlist', __name__)

@wishlist_bp.route('/wishlist', methods=['POST'])
@jwt_required()
def add_to_wishlist():
    user_id = get_jwt_identity()  # Get the current user's identity from the JWT
    data = request.get_json()
    
    # Validate input data
    if 'product_id' not in data:
        return jsonify({'error': 'Missing product_id'}), 400
    
    # Create a new wishlist item
    wishlist_item = Wishlist(user_id=user_id, product_id=data['product_id'])
    db.session.add(wishlist_item)
    db.session.commit()
    
    return jsonify({"message": "Added to wishlist"}), 201

@wishlist_bp.route('/wishlist', methods=['GET'])
@jwt_required()
def get_wishlist():
    user_id = get_jwt_identity()  # Get the current user's identity from the JWT
    items = Wishlist.query.filter_by(user_id=user_id).all()
    
    # Serialize each item in the wishlist
    return jsonify([item.to_dict() for item in items]), 200
