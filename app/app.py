"""
Flask Application for Task 2: Database App

Flask application with PostgreSQL database integration.
Features:
- Database connection and models
- UI to display tables and records
- RESTful API endpoints
"""
from flask import Flask, jsonify, render_template
from decouple import config
import logging
import os

# Import database
from models import db, init_db

# Import blueprints
from routes.api import api_bp
from routes.database import db_bp

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app():
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Database configuration
    database_url = config('DATABASE_URL', default=None)
    if not database_url:
        # Construct from individual components
        db_user = config('DB_USER', default='flaskuser')
        db_password = config('DB_PASSWORD', default='flaskpass')
        db_host = config('DB_HOST', default='localhost')
        db_port = config('DB_PORT', default='5432', cast=str)
        db_name = config('DB_NAME', default='flaskdb')
        database_url = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
    
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize database
    init_db(app)
    
    # Register blueprints
    app.register_blueprint(api_bp)
    app.register_blueprint(db_bp)
    
    @app.route('/')
    def home():
        """Home page - redirects to database UI"""
        return render_template('index.html')
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Endpoint not found"}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({"error": "Internal server error"}), 500
    
    return app

app = create_app()
PORT = config('PORT', default=5000, cast=int)

if __name__ == '__main__':
    logger.info(f"Starting Flask app on port {PORT}")
    app.run(host='0.0.0.0', port=PORT, debug=True)

