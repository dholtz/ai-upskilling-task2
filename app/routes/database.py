"""Database routes for displaying tables and records"""
from flask import Blueprint, render_template, jsonify, request, flash, redirect, url_for
from werkzeug.utils import secure_filename
from models import db, User, Product, PresentationFile, PresentationSlide, SlideUrl
from utils.pptx_parser import extract_text_and_urls
import logging
import os
from datetime import datetime

logger = logging.getLogger(__name__)

db_bp = Blueprint('database', __name__, url_prefix='/db')

# Allowed file extensions
ALLOWED_EXTENSIONS = {'pptx'}
UPLOAD_FOLDER = '/tmp/uploads'  # Temporary upload folder in container (mounted volume)

@db_bp.route('/')
def index():
    """Database UI home page"""
    return render_template('database.html')

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@db_bp.route('/tables')
def list_tables():
    """Get list of all tables (only showing presentation-related tables)"""
    tables = [
        {'name': 'presentation_files', 'display_name': 'Uploaded Files', 'count': PresentationFile.query.count()},
        {'name': 'presentation_slides', 'display_name': 'Presentation Slides', 'count': PresentationSlide.query.count()},
        {'name': 'slide_urls', 'display_name': 'Slide URLs', 'count': SlideUrl.query.count()}
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
        elif table_name == 'presentation_files':
            records = PresentationFile.query.order_by(PresentationFile.uploaded_at.desc()).all()
            data = [record.to_dict() for record in records]
        elif table_name == 'presentation_slides':
            records = PresentationSlide.query.order_by(PresentationSlide.slide_number).all()
            data = [record.to_dict() for record in records]
        elif table_name == 'slide_urls':
            records = SlideUrl.query.all()
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
        elif table_name == 'presentation_files':
            record = PresentationFile.query.get_or_404(record_id)
        elif table_name == 'presentation_slides':
            record = PresentationSlide.query.get_or_404(record_id)
        elif table_name == 'slide_urls':
            record = SlideUrl.query.get_or_404(record_id)
        else:
            return jsonify({'error': f'Table {table_name} not found'}), 404
        
        return jsonify({
            'table': table_name,
            'record': record.to_dict()
        })
    except Exception as e:
        logger.error(f"Error fetching record: {str(e)}")
        return jsonify({'error': str(e)}), 500

@db_bp.route('/upload', methods=['GET', 'POST'])
def upload_pptx():
    """Upload and parse a PowerPoint file"""
    if request.method == 'GET':
        return render_template('upload.html')
    
    # Check if file was uploaded
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Only .pptx files are allowed'}), 400
    
    try:
        # Create upload directory if it doesn't exist
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        
        # Save uploaded file
        original_filename = file.filename
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        # Parse the PowerPoint file
        logger.info(f"Parsing PowerPoint file: {filepath}")
        slides_data = extract_text_and_urls(filepath)
        
        # Create or get PresentationFile record
        presentation_file = PresentationFile(
            filename=filename,
            original_filename=original_filename,
            uploaded_at=datetime.utcnow()
        )
        db.session.add(presentation_file)
        db.session.flush()  # Get the file ID
        
        # Save to database
        saved_count = 0
        url_count = 0
        
        for slide_data in slides_data:
            # Create slide record
            slide = PresentationSlide(
                slide_number=slide_data['slide_number'],
                text=slide_data['text'],
                source_file=filename,  # Keep for backward compatibility
                file_id=presentation_file.id
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
        
        # Update file counts
        presentation_file.slide_count = saved_count
        presentation_file.url_count = url_count
        
        db.session.commit()
        
        # Clean up uploaded file
        os.remove(filepath)
        
        return jsonify({
            'message': 'File uploaded and parsed successfully',
            'slides_imported': saved_count,
            'urls_extracted': url_count,
            'filename': filename,
            'file_id': presentation_file.id
        }), 200
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error processing file: {str(e)}")
        return jsonify({'error': f'Error processing file: {str(e)}'}), 500

@db_bp.route('/test-parse', methods=['POST'])
def test_parse():
    """Test endpoint to debug PowerPoint parsing"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type'}), 400
    
    try:
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        # Parse and return detailed info
        slides_data = extract_text_and_urls(filepath)
        
        # Clean up
        os.remove(filepath)
        
        # Return detailed parsing results
        result = {
            'total_slides': len(slides_data),
            'total_urls': sum(len(slide['urls']) for slide in slides_data),
            'slides': []
        }
        
        for slide in slides_data:
            result['slides'].append({
                'slide_number': slide['slide_number'],
                'text_preview': slide['text'][:100] + '...' if len(slide['text']) > 100 else slide['text'],
                'url_count': len(slide['urls']),
                'urls': slide['urls']
            })
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Error in test parse: {str(e)}")
        import traceback
        return jsonify({
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500

@db_bp.route('/clear', methods=['POST'])
def clear_database():
    """Clear presentation-related tables (slides and URLs)"""
    try:
        # Count records before deletion
        file_count = PresentationFile.query.count()
        slide_count = PresentationSlide.query.count()
        url_count = SlideUrl.query.count()
        
        # Delete all URLs first (due to foreign key constraint)
        SlideUrl.query.delete()
        # Delete all slides
        PresentationSlide.query.delete()
        # Delete all files
        PresentationFile.query.delete()
        
        db.session.commit()
        
        logger.info(f"Cleared database: {file_count} files, {slide_count} slides and {url_count} URLs removed")
        
        return jsonify({
            'message': 'Database cleared successfully',
            'files_deleted': file_count,
            'slides_deleted': slide_count,
            'urls_deleted': url_count
        }), 200
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error clearing database: {str(e)}")
        return jsonify({'error': f'Error clearing database: {str(e)}'}), 500

@db_bp.route('/files', methods=['GET'])
def list_files():
    """Get list of all uploaded files"""
    try:
        files = PresentationFile.query.order_by(PresentationFile.uploaded_at.desc()).all()
        data = [file.to_dict() for file in files]
        return jsonify({'files': data, 'count': len(data)}), 200
    except Exception as e:
        logger.error(f"Error fetching files: {str(e)}")
        return jsonify({'error': str(e)}), 500

@db_bp.route('/files/<int:file_id>', methods=['DELETE'])
def delete_file_data(file_id):
    """Delete all data associated with a specific file"""
    try:
        presentation_file = PresentationFile.query.get_or_404(file_id)
        
        # Count what will be deleted
        slide_count = presentation_file.slide_count
        url_count = presentation_file.url_count
        
        # Delete all URLs for slides in this file
        slide_ids = [slide.id for slide in presentation_file.slides]
        SlideUrl.query.filter(SlideUrl.slide_id.in_(slide_ids)).delete()
        
        # Delete all slides for this file
        PresentationSlide.query.filter_by(file_id=file_id).delete()
        
        # Delete the file record
        db.session.delete(presentation_file)
        db.session.commit()
        
        logger.info(f"Deleted file {presentation_file.filename}: {slide_count} slides and {url_count} URLs removed")
        
        return jsonify({
            'message': f'File "{presentation_file.original_filename}" deleted successfully',
            'slides_deleted': slide_count,
            'urls_deleted': url_count
        }), 200
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error deleting file: {str(e)}")
        return jsonify({'error': f'Error deleting file: {str(e)}'}), 500

