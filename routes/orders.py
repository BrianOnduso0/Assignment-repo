from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from models import Order, Product

# Create blueprint for orders
order_bp = Blueprint('orders', __name__)

# Create a new order
@order_bp.route('/orders', methods=['POST'])
@jwt_required()
def create_order():
    data = request.get_json()
    user_id = get_jwt_identity()
    
    if not data or not 'products' in data:
        return jsonify({'error': 'Missing data'}), 400
    
    total_amount = 0
    for product_data in data['products']:
        product = Product.query.get(product_data['product_id'])
        if not product:
            return jsonify({'error': f"Product with id {product_data['product_id']} not found"}), 404
        total_amount += product_data['quantity'] * product.price

    new_order = Order(
        user_id=user_id,
        total_amount=total_amount,
        status='Pending'
    )
    
    db.session.add(new_order)
    db.session.commit()

    return jsonify(new_order.to_dict()), 201

# Get all orders for the logged-in user
@order_bp.route('/orders', methods=['GET'])
@jwt_required()
def get_orders():
    user_id = get_jwt_identity()
    orders = Order.query.filter_by(user_id=user_id).all()
    return jsonify([order.to_dict() for order in orders]), 200

# Update order status
@order_bp.route('/orders/<int:id>', methods=['PUT'])
@jwt_required()
def update_order_status(id):
    order = Order.query.get_or_404(id)
    data = request.get_json()

    if 'status' in data:
        order.status = data['status']

    db.session.commit()

    return jsonify(order.to_dict()), 200

# Delete an order
@order_bp.route('/orders/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_order(id):
    order = Order.query.get_or_404(id)
    
    db.session.delete(order)
    db.session.commit()

    return jsonify({'message': 'Order deleted'}), 204
