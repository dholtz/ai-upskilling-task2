"""Database table models"""
from .database import db
from datetime import datetime

class PresentationFile(db.Model):
    """Track uploaded PowerPoint files"""
    __tablename__ = 'presentation_files'
    
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    slide_count = db.Column(db.Integer, default=0)
    url_count = db.Column(db.Integer, default=0)
    
    # Relationships
    slides = db.relationship('PresentationSlide', backref='file', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'filename': self.filename,
            'original_filename': self.original_filename,
            'uploaded_at': self.uploaded_at.isoformat() if self.uploaded_at else None,
            'slide_count': self.slide_count,
            'url_count': self.url_count
        }
    
    def __repr__(self):
        return f'<PresentationFile {self.filename}>'

class User(db.Model):
    """User table model"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<User {self.username}>'

class Product(db.Model):
    """Product table model"""
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    stock = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': float(self.price) if self.price else 0.0,
            'stock': self.stock,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<Product {self.name}>'

class PresentationSlide(db.Model):
    """Presentation slide data extracted from .pptx files"""
    __tablename__ = 'presentation_slides'
    
    id = db.Column(db.Integer, primary_key=True)
    slide_number = db.Column(db.Integer, nullable=False)
    text = db.Column(db.Text)
    source_file = db.Column(db.String(255))  # Keep for backward compatibility
    file_id = db.Column(db.Integer, db.ForeignKey('presentation_files.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship to URLs
    urls = db.relationship('SlideUrl', backref='slide', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'slide_number': self.slide_number,
            'text': self.text,
            'source_file': self.source_file,
            'file_id': self.file_id,
            'file_name': self.file.original_filename if self.file else self.source_file,
            'urls': [url.to_dict() for url in self.urls],
            'url_count': len(self.urls),
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<PresentationSlide {self.slide_number}>'

class SlideUrl(db.Model):
    """URLs extracted from presentation slides"""
    __tablename__ = 'slide_urls'
    
    id = db.Column(db.Integer, primary_key=True)
    slide_id = db.Column(db.Integer, db.ForeignKey('presentation_slides.id'), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    link_text = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'url': self.url,
            'link_text': self.link_text,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<SlideUrl {self.url[:50]}>'

