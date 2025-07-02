from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_migrate import Migrate
import os

app = Flask(__name__)

# CORS configuration
CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}})

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI', 'sqlite:///ecommerce.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# JWT configuration
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'your_default_secret_key')  # Use an environment variable or a secure key
app.config['SESSION_COOKIE_SAMESITE'] = 'None'  # For CORS
app.config['SESSION_COOKIE_SECURE'] = True  # Ensure you're using HTTPS in production

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# Import blueprints after app initialization to avoid circular imports
from routes.authRoutes import auth_bp
from routes.productRoute import product_bp
from routes.wishlist import wishlist_bp
from routes.cart import cart_bp
from routes.orders import order_bp
from routes.payments import payment_bp
from routes.reviews import review_bp

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(product_bp)
app.register_blueprint(wishlist_bp)
app.register_blueprint(cart_bp)
app.register_blueprint(order_bp)
app.register_blueprint(payment_bp)
app.register_blueprint(review_bp)

if __name__ == '__main__':
    app.run(debug=True)
