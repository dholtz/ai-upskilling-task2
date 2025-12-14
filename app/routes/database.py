"""Database routes for displaying tables and records"""
from flask import Blueprint, render_template, jsonify, request
from models import db, User, Product
import logging

logger = logging.getLogger(__name__)

db_bp = Blueprint('database', __name__, url_prefix='/db')

@db_bp.route('/')
def index():
    """Database UI home page"""
    return render_template('database.html')

@db_bp.route('/tables')
def list_tables():
    """Get list of all tables"""
    tables = [
        {'name': 'users', 'display_name': 'Users', 'count': User.query.count()},
        {'name': 'products', 'display_name': 'Products', 'count': Product.query.count()}
    ]
    return jsonify({'tables': tables})

@db_bp.route('/table/<table_name>')
def get_table_data(table_name):
    """Get all records from a specific table"""
    try:
        if table_name == 'users':
            records = User.query.all()
            data = [record.to_dict() for record in records]
        elif table_name == 'products':
            records = Product.query.all()
            data = [record.to_dict() for record in records]
        else:
            return jsonify({'error': f'Table {table_name} not found'}), 404
        
        return jsonify({
            'table': table_name,
            'count': len(data),
            'records': data
        })
    except Exception as e:
        logger.error(f"Error fetching table data: {str(e)}")
        return jsonify({'error': str(e)}), 500

@db_bp.route('/table/<table_name>/record/<int:record_id>')
def get_record(table_name, record_id):
    """Get a specific record by ID"""
    try:
        if table_name == 'users':
            record = User.query.get_or_404(record_id)
        elif table_name == 'products':
            record = Product.query.get_or_404(record_id)
        else:
            return jsonify({'error': f'Table {table_name} not found'}), 404
        
        return jsonify({
            'table': table_name,
            'record': record.to_dict()
        })
    except Exception as e:
        logger.error(f"Error fetching record: {str(e)}")
        return jsonify({'error': str(e)}), 500

