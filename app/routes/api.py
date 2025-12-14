from flask import Blueprint, request, jsonify
import logging

logger = logging.getLogger(__name__)

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    from models import db
    try:
        # Test database connection
        db.session.execute(db.text('SELECT 1'))
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"
    
    return jsonify({
        "status": "healthy", 
        "service": "flask-app",
        "database": db_status
    }), 200

@api_bp.route('/example', methods=['GET', 'POST'])
def example():
    """Example endpoint for AI upskilling exercises"""
    if request.method == 'GET':
        return jsonify({
            "message": "This is an example endpoint",
            "usage": "Add your AI/ML functionality here",
            "methods": ["GET", "POST"]
        }), 200
    
    # POST example
    data = request.get_json() or {}
    return jsonify({
        "message": "Received data",
        "data": data,
        "note": "This is where you'd process data with AI/ML models"
    }), 200

