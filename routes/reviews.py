from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from models import Review, Product, User

# Create blueprint for reviews
review_bp = Blueprint('reviews', __name__)

# Create a review
@review_bp.route('/reviews', methods=['POST'])
@jwt_required()
def create_review():
    data = request.get_json()
    user_id = get_jwt_identity()
    
    if not data or not all(k in data for k in ('product_id', 'rating', 'comment')):
        return jsonify({'error': 'Missing data'}), 400

    new_review = Review(
        user_id=user_id,
        product_id=data['product_id'],
        rating=data['rating'],
        comment=data['comment']
    )
    
    db.session.add(new_review)
    db.session.commit()
    
    return jsonify(new_review.to_dict()), 201

# Get all reviews for a product
@review_bp.route('/products/<int:product_id>/reviews', methods=['GET'])
def get_product_reviews(product_id):
    reviews = Review.query.filter_by(product_id=product_id).all()
    return jsonify([review.to_dict() for review in reviews]), 200

# Edit a review
@review_bp.route('/reviews/<int:id>', methods=['PUT'])
@jwt_required()
def update_review(id):
    review = Review.query.get_or_404(id)
    user_id = get_jwt_identity()
    
    if review.user_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()

    if 'rating' in data:
        review.rating = data['rating']
    if 'comment' in data:
        review.comment = data['comment']

    db.session.commit()

    return jsonify(review.to_dict()), 200

# Delete a review
@review_bp.route('/reviews/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_review(id):
    review = Review.query.get_or_404(id)
    user_id = get_jwt_identity()

    if review.user_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    db.session.delete(review)
    db.session.commit()

    return jsonify({'message': 'Review deleted'}), 204
