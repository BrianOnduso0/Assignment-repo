from app import db
from datetime import datetime
from sqlalchemy import Enum
import enum

# Enum for Payment Status
class PaymentStatus(enum.Enum):
    pending = "pending"
    completed = "completed"
    failed = "failed"

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    # Relationships
    wishlist = db.relationship('Wishlist', backref='user', lazy=True)
    cart = db.relationship('Cart', backref='user', lazy=True)
    payments = db.relationship('Payment', backref='user', lazy=True)

    # Serialization method
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'wishlist': [item.to_dict() for item in self.wishlist],
            'cart': [item.to_dict() for item in self.cart],
            'payments': [payment.to_dict() for payment in self.payments]
        }

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0) 
    price = db.Column(db.Numeric(10, 2), nullable=False)  # Use Decimal for better precision
    description = db.Column(db.String(500))  # Increased size for longer descriptions

    # Relationships
    wishlist_items = db.relationship('Wishlist', backref='product', lazy=True)
    cart_items = db.relationship('Cart', backref='product', lazy=True)

    # Serialization method
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'quantity': self.quantity,
            'price': float(self.price),  # Convert Decimal to float for easier JSON serialization
            'description': self.description
        }

class Wishlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

    # Serialization method
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'product': self.product.to_dict()
        }

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    # Serialization method
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'product': self.product.to_dict(),
            'quantity': self.quantity
        }

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(Enum(PaymentStatus), nullable=False)

    # Serialization method
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'amount': float(self.amount),  # Convert Decimal to float for easier JSON serialization
            'status': self.status.value  # Return the enum value as a string
        }

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default='Pending')

    # Serialize method
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'total_amount': self.total_amount,
            'created_at': self.created_at,
            'status': self.status
        }
    
class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Serialize method
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'product_id': self.product_id,
            'rating': self.rating,
            'comment': self.comment,
            'created_at': self.created_at
        }