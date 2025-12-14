# Application Architecture Documentation

This document provides a comprehensive overview of the critical components that make this Flask-based PowerPoint parsing and database application function.

## Table of Contents

1. [Overview](#overview)
2. [System Architecture](#system-architecture)
3. [Database Layer](#database-layer)
4. [Application Layer](#application-layer)
5. [Frontend Layer](#frontend-layer)
6. [PowerPoint Parsing Engine](#powerpoint-parsing-engine)
7. [Deployment Architecture](#deployment-architecture)
8. [Data Flow](#data-flow)
9. [Key Technologies](#key-technologies)

---

## Overview

This application is a **Flask-based web application** that:
- Accepts PowerPoint (`.pptx`) file uploads via a web interface
- Extracts text content and hyperlinks from each slide
- Stores the extracted data in a PostgreSQL database
- Provides a web UI to view, manage, and interact with the stored data
- Runs in a containerized environment using Docker Compose

---

## System Architecture

The application follows a **three-tier architecture**:

```
┌─────────────────────────────────────────┐
│         Frontend (Browser)              │
│  - HTML/CSS/JavaScript                  │
│  - Database viewer UI                   │
│  - File upload interface                │
└──────────────┬──────────────────────────┘
               │ HTTP/REST API
┌──────────────▼──────────────────────────┐
│      Application Layer (Flask)          │
│  - Routes & Blueprints                  │
│  - Business Logic                       │
│  - PowerPoint Parser                    │
│  - SQLAlchemy ORM                       │
└──────────────┬──────────────────────────┘
               │ SQL
┌──────────────▼──────────────────────────┐
│      Database Layer (PostgreSQL)        │
│  - Relational Data Storage              │
│  - Foreign Key Relationships            │
└─────────────────────────────────────────┘
```

---

## Database Layer

### Database Engine
- **PostgreSQL 15** (Alpine Linux variant for smaller image size)
- Containerized and managed via Docker Compose
- Persistent storage via Docker volumes

### Database Models (`app/models/tables.py`)

The application uses **SQLAlchemy ORM** to define four main data models:

#### 1. `PresentationFile`
Tracks metadata about uploaded PowerPoint files:
- `id` - Primary key
- `filename` - Sanitized filename (safe for filesystem)
- `original_filename` - Original uploaded filename
- `uploaded_at` - Timestamp of upload
- `slide_count` - Number of slides extracted
- `url_count` - Total URLs extracted from all slides
- **Relationship**: One-to-many with `PresentationSlide` (cascade delete)

#### 2. `PresentationSlide`
Stores extracted content from individual slides:
- `id` - Primary key
- `slide_number` - Position in presentation (1-indexed)
- `text` - All text content extracted from the slide
- `source_file` - Filename (backward compatibility)
- `file_id` - Foreign key to `presentation_files.id`
- `created_at` - Timestamp
- **Relationships**: 
  - Many-to-one with `PresentationFile`
  - One-to-many with `SlideUrl` (cascade delete)

#### 3. `SlideUrl`
Stores hyperlinks extracted from slides:
- `id` - Primary key
- `slide_id` - Foreign key to `presentation_slides.id`
- `url` - The extracted URL (HTTP/HTTPS/mailto)
- `link_text` - Associated text or anchor text
- `created_at` - Timestamp
- **Relationship**: Many-to-one with `PresentationSlide`

#### 4. `User` and `Product` (Legacy)
Example models for demonstration purposes (not actively used in PowerPoint workflow).

### Database Initialization (`app/models/database.py`)

- Uses **Flask-SQLAlchemy** for database abstraction
- `init_db(app)` function creates all tables on startup
- Tables are created automatically via `db.create_all()` when the app starts

### Database Connection

Connection is configured via environment variables:
- `DATABASE_URL` (full connection string) OR
- Individual components: `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`, `DB_NAME`
- Defaults provided for local development

---

## Application Layer

### Flask Application Factory (`app/app.py`)

The application uses the **Application Factory Pattern**:

```python
def create_app():
    # Configure database
    # Register blueprints
    # Set up error handlers
    return app
```

**Key Responsibilities:**
1. **Database Configuration**: Constructs PostgreSQL connection string from environment variables
2. **Blueprint Registration**: Registers route blueprints for modular organization
3. **Error Handling**: Global 404 and 500 error handlers
4. **Logging**: Configures application-wide logging

### Route Blueprints

The application is organized into **two main blueprints**:

#### 1. API Blueprint (`app/routes/api.py`)
- **Prefix**: `/api`
- **Endpoints**:
  - `GET /api/health` - Health check with database connectivity test
  - `GET/POST /api/example` - Example endpoint for AI/ML integration

#### 2. Database Blueprint (`app/routes/database.py`)
- **Prefix**: `/db`
- **Endpoints**:
  - `GET /db/` - Main database UI page
  - `GET /db/tables` - List all available tables with record counts
  - `GET /db/table/<table_name>` - Get all records from a table
  - `GET /db/table/<table_name>/record/<id>` - Get specific record by ID
  - `GET /db/files` - List all uploaded PowerPoint files
  - `POST /db/upload` - Upload and parse PowerPoint file(s)
  - `POST /db/clear` - Clear all presentation data
  - `DELETE /db/files/<file_id>` - Delete specific file and all related data
  - `POST /db/test-parse` - Debug endpoint for PowerPoint parsing

**Key Features:**
- **File Upload Handling**: Accepts multiple `.pptx` files
- **File Validation**: Checks file extension and handles errors
- **Transaction Management**: Uses database transactions with rollback on errors
- **Cascade Deletion**: Deleting a file automatically removes related slides and URLs
- **Temporary File Management**: Uploads stored in `/tmp/uploads` and cleaned up after processing

### PowerPoint Parser (`app/utils/pptx_parser.py`)

**Critical Component**: The `extract_text_and_urls()` function is the core parsing engine.

**How It Works:**
1. Opens PowerPoint file using `python-pptx` library
2. Iterates through each slide
3. For each slide, processes all shapes:
   - **Text Extraction**: Collects text from shapes, text frames, and table cells
   - **Hyperlink Extraction**: Multiple methods to find URLs:
     - Direct hyperlink attributes on text runs
     - XML relationship IDs (rId) resolved through slide relationships
     - Table cell hyperlinks
     - Shape click actions
     - Paragraph-level hyperlinks
4. Deduplicates URLs per slide (avoids counting same URL multiple times)
5. Filters out internal links (starting with `#`)
6. Returns structured data: `[{slide_number, text, urls: [{url, text}]}]`

**Complexity**: The parser handles edge cases like:
- Hyperlinks stored as relationship IDs in XML
- Hyperlinks in table cells
- Group shapes (which cannot have click actions)
- Multiple hyperlink storage formats in PowerPoint files

---

## Frontend Layer

### Main UI (`app/templates/database.html`)

The primary user interface provides:
- **File Upload Section**: Multi-file upload with drag-and-drop support
- **Uploaded Files List**: Table showing all files with metadata and delete actions
- **Table Cards**: Clickable cards for each database table showing record counts
- **Data Tables**: Dynamic tables displaying records when a table is selected
- **Clickable URLs**: All URLs in the Slide URLs table are rendered as clickable links

### JavaScript (`app/static/js/database.js`)

**Key Functions:**
- `loadTables()` - Fetches and displays available tables
- `loadFiles()` - Loads and displays uploaded files
- `loadTableData(tableName)` - Fetches and displays records from a table
- `setupUploadForm()` - Handles file upload with progress feedback
- `deleteFile(fileId)` - Deletes a file and refreshes the UI
- `clearAllData()` - Clears all presentation data

**Features:**
- **Async/Await**: Modern JavaScript for API calls
- **Error Handling**: User-friendly error messages
- **UI Updates**: Dynamic DOM manipulation without page reloads
- **URL Rendering**: Converts URLs to clickable `<a>` tags with `target="_blank"`

### Styling (`app/static/css/style.css`)

Provides modern, responsive styling for:
- Card-based layout
- Data tables
- Upload interface
- Status messages (success/error/loading)

---

## PowerPoint Parsing Engine

### Detailed Workflow

1. **File Upload** (`POST /db/upload`):
   - Validates file extension (`.pptx` only)
   - Saves file to `/tmp/uploads` with sanitized filename
   - Calls `extract_text_and_urls(filepath)`

2. **Parsing Process** (`app/utils/pptx_parser.py`):
   - Opens PowerPoint using `python-pptx`
   - For each slide:
     - Processes all shapes (text boxes, images, tables, etc.)
     - Extracts text content
     - Finds hyperlinks at multiple levels (run, paragraph, shape)
     - Resolves relationship IDs to actual URLs
     - Deduplicates URLs
   - Returns list of slide dictionaries

3. **Database Storage**:
   - Creates `PresentationFile` record
   - For each slide: Creates `PresentationSlide` record
   - For each URL: Creates `SlideUrl` record with foreign key
   - Updates file metadata (slide_count, url_count)
   - Commits transaction

4. **Cleanup**:
   - Deletes temporary uploaded file
   - Returns success response with statistics

### Hyperlink Resolution

PowerPoint files store hyperlinks in multiple ways:
- **Direct Address**: `hyperlink.address` contains the URL directly
- **Relationship ID**: Hyperlink references an `rId` that must be resolved through the slide's relationship collection
- The parser handles both cases and falls back gracefully

---

## Deployment Architecture

### Docker Compose Setup (`docker-compose.yml`)

**Two Services:**

#### 1. Database Service (`db`)
- Image: `postgres:15-alpine`
- Port: `5432` (configurable)
- Volume: `postgres_data` for persistent storage
- Health Check: `pg_isready` command
- Environment: Database credentials from `.env` or defaults

#### 2. Application Service (`app`)
- Built from `app/Dockerfile`
- Port: `5000` (configurable)
- Depends on: Database service (waits for health check)
- Volumes:
  - App code (for hot-reload in development)
  - Upload directory (`./uploads:/tmp/uploads`)
  - Corporate CA certificate (for SSL/TLS in corporate environments)
- Entrypoint: 
  1. Waits 5 seconds for DB to be ready
  2. Runs `init_db.py` to create tables
  3. Starts Gunicorn WSGI server

### Dockerfile (`app/Dockerfile`)

**Key Features:**
- Base: `python:3.9-slim`
- **Corporate CA Certificate**: Adds custom CA certificate to trust store (for environments behind corporate proxies)
- **SSL Configuration**: Sets environment variables for Python, pip, requests to use updated CA bundle
- **Dependencies**: Installs from `requirements.txt`
- **Health Check**: HTTP endpoint check
- **Production Server**: Uses Gunicorn (not Flask dev server)

### Network Architecture

- **Bridge Network**: `app-network` connects both containers
- **Service Discovery**: App connects to database using service name `db` (Docker DNS)

---

## Data Flow

### Upload Flow

```
User selects .pptx file(s)
    ↓
JavaScript: FormData → POST /db/upload
    ↓
Flask Route: Validates file, saves to /tmp/uploads
    ↓
pptx_parser.extract_text_and_urls()
    ↓
Returns: [{slide_number, text, urls: [...]}]
    ↓
Database Transaction:
  - Create PresentationFile
  - For each slide: Create PresentationSlide
  - For each URL: Create SlideUrl
  - Update file counts
  - Commit
    ↓
Delete temporary file
    ↓
Return JSON response with statistics
    ↓
JavaScript: Refresh UI (tables, files list)
```

### View Data Flow

```
User clicks table card
    ↓
JavaScript: GET /db/table/<table_name>
    ↓
Flask Route: Query database using SQLAlchemy
    ↓
Convert models to dictionaries (to_dict())
    ↓
Return JSON: {table, count, records: [...]}
    ↓
JavaScript: Render table in UI
```

### Delete Flow

```
User clicks delete button
    ↓
JavaScript: DELETE /db/files/<file_id>
    ↓
Flask Route: 
  - Find PresentationFile by ID
  - Delete file (cascade deletes slides and URLs)
  - Commit transaction
    ↓
Return success response
    ↓
JavaScript: Refresh files list and tables
```

---

## Key Technologies

### Backend
- **Flask 2.0+**: Web framework
- **SQLAlchemy 2.0+**: ORM for database operations
- **Flask-SQLAlchemy**: Flask integration for SQLAlchemy
- **psycopg2-binary**: PostgreSQL adapter
- **python-pptx**: PowerPoint file parsing
- **python-decouple**: Environment variable management
- **Gunicorn**: Production WSGI server

### Frontend
- **Vanilla JavaScript**: No framework dependencies
- **Fetch API**: For HTTP requests
- **Modern CSS**: Responsive design

### Infrastructure
- **Docker**: Containerization
- **Docker Compose**: Multi-container orchestration
- **PostgreSQL 15**: Database
- **Alpine Linux**: Lightweight base images

### Development Tools
- **Make**: Build automation (see `app/Makefile`)
- **Health Checks**: Container health monitoring
- **Logging**: Python logging module

---

## Critical Design Decisions

1. **Cascade Deletes**: Deleting a `PresentationFile` automatically removes all related slides and URLs, preventing orphaned records.

2. **Temporary File Storage**: Files are stored in `/tmp/uploads` and immediately deleted after parsing to save disk space.

3. **Transaction Safety**: All database operations use transactions with rollback on errors to maintain data consistency.

4. **Multi-file Upload**: The frontend supports uploading multiple files sequentially, providing feedback for each.

5. **Relationship Resolution**: The PowerPoint parser handles complex hyperlink storage formats, including XML relationship IDs.

6. **Application Factory Pattern**: Allows for better testing and configuration management.

7. **Blueprint Organization**: Routes are organized into logical blueprints for maintainability.

8. **Corporate Proxy Support**: Dockerfile includes corporate CA certificate handling for enterprise environments.

---

## Security Considerations

- **File Validation**: Only `.pptx` files are accepted
- **Filename Sanitization**: Uses `werkzeug.utils.secure_filename()` to prevent path traversal
- **SQL Injection Prevention**: SQLAlchemy ORM prevents SQL injection
- **Error Handling**: Errors don't expose sensitive information to users
- **Temporary Files**: Uploaded files are deleted immediately after processing

---

## Extension Points

The application is designed to be extended:

1. **AI/ML Integration**: The `/api/example` endpoint is a placeholder for AI/ML functionality
2. **Additional File Types**: The parser can be extended to support other formats
3. **Authentication**: Can be added via Flask extensions (Flask-Login, etc.)
4. **Search/Filter**: Can be added to the frontend JavaScript
5. **Export Functionality**: Can add CSV/JSON export endpoints
6. **Slide Thumbnails**: Can extract and store slide images

---

This architecture provides a solid foundation for a PowerPoint parsing and database application with clear separation of concerns and extensibility.
