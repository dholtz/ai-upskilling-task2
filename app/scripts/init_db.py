"""Script to initialize database with sample data or parse PowerPoint file"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from models import db, PresentationFile, PresentationSlide, SlideUrl
from utils.pptx_parser import extract_text_and_urls
from datetime import datetime

def init_sample_data():
    """Initialize database with sample data (legacy function - not currently used)"""
    app = create_app()
    
    with app.app_context():
        # Clear existing data
        db.drop_all()
        db.create_all()
        
        db.session.commit()
        print("✅ Database initialized (empty, ready for uploads)")

def init_from_pptx(pptx_path):
    """Initialize database from PowerPoint file"""
    app = create_app()
    
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()
        
        # Parse PowerPoint file
        print(f"📄 Parsing PowerPoint file: {pptx_path}")
        slides_data = extract_text_and_urls(pptx_path)
        
        # Get filename
        filename = os.path.basename(pptx_path)
        
        # Save to database
        saved_count = 0
        url_count = 0
        
        for slide_data in slides_data:
            # Create slide record
            slide = PresentationSlide(
                slide_number=slide_data['slide_number'],
                text=slide_data['text'],
                source_file=filename
            )
            db.session.add(slide)
            db.session.flush()  # Get the slide ID
            
            # Create URL records
            for url_data in slide_data['urls']:
                url_record = SlideUrl(
                    slide_id=slide.id,
                    url=url_data['url'],
                    link_text=url_data.get('text', '')
                )
                db.session.add(url_record)
                url_count += 1
            
            saved_count += 1
        
        db.session.commit()
        print("✅ PowerPoint data imported!")
        print(f"   - {saved_count} slides imported")
        print(f"   - {url_count} URLs extracted")

if __name__ == '__main__':
    # Check if PowerPoint file path is provided
    if len(sys.argv) > 1:
        pptx_path = sys.argv[1]
        if os.path.exists(pptx_path):
            init_from_pptx(pptx_path)
        else:
            print(f"❌ Error: File not found: {pptx_path}")
            sys.exit(1)
    else:
        # Default: just create tables (no sample data)
        # Users can upload .pptx files via the UI
        app = create_app()
        with app.app_context():
            db.create_all()
            print("✅ Database tables created (ready for uploads)")

