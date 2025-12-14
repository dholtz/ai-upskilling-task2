"""Script to initialize database with sample data"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from models import db, User, Product
from datetime import datetime

def init_sample_data():
    """Initialize database with sample data"""
    app = create_app()
    
    with app.app_context():
        # Clear existing data
        db.drop_all()
        db.create_all()
        
        # Add sample users
        users = [
            User(username='alice', email='alice@example.com'),
            User(username='bob', email='bob@example.com'),
            User(username='charlie', email='charlie@example.com'),
        ]
        
        for user in users:
            db.session.add(user)
        
        # Add sample products
        products = [
            Product(name='Laptop', description='High-performance laptop', price=999.99, stock=15),
            Product(name='Mouse', description='Wireless mouse', price=29.99, stock=50),
            Product(name='Keyboard', description='Mechanical keyboard', price=79.99, stock=30),
            Product(name='Monitor', description='27-inch 4K monitor', price=399.99, stock=10),
        ]
        
        for product in products:
            db.session.add(product)
        
        db.session.commit()
        print("✅ Sample data initialized!")
        print(f"   - {len(users)} users created")
        print(f"   - {len(products)} products created")

if __name__ == '__main__':
    init_sample_data()

