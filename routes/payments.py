from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app import db
from models import Payment  # Make sure to import the Payment model
# Assuming you have these functions implemented elsewhere
# from your_mpesa_module import initiate_mpesa_stk_push, process_mpesa_payment  

# Create blueprint for payment routes
payment_bp = Blueprint('payment', __name__)

@payment_bp.route('/payments/mpesa', methods=['POST'])
@jwt_required()
def mpesa_payment():
    data = request.get_json()
    
    # Validate input data
    if 'phone_number' not in data or 'amount' not in data:
        return jsonify({'error': 'Missing phone_number or amount'}), 400

    phone_number = data['phone_number']
    amount = data['amount']

    # Trigger MPESA STK Push
    response = initiate_mpesa_stk_push(phone_number, amount)

    # You may want to save the payment status in your database
    payment = Payment(user_id=get_jwt_identity(), amount=amount, status=response.get('status', 'pending'))
    db.session.add(payment)
    db.session.commit()
    
    return jsonify(response), 200

@payment_bp.route('/payments/callback', methods=['POST'])
def mpesa_callback():
    # Handle MPESA payment callback here
    callback_data = request.get_json()

    # Process the callback data
    process_mpesa_payment(callback_data)

    return jsonify({"message": "Callback received"}), 200
