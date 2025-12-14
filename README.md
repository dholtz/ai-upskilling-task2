# Task 2: Database App

Flask application with PostgreSQL database integration. This project demonstrates deploying two containers (APP and DB) with a web UI to view database tables and records.

## Features

- ✅ **PostgreSQL Database** - Containerized PostgreSQL 15
- ✅ **Flask Application** - Containerized Flask app with database integration
- ✅ **Web UI** - Interactive interface to view tables and records
- ✅ **Docker Compose** - Multi-container orchestration
- ✅ **PowerPoint Parser** - Upload and parse .pptx files to extract text and URLs
- ✅ **Multi-File Management** - Upload and manage multiple PowerPoint files
- ✅ **Clickable Links** - All URLs in tables are clickable and open in new tabs

## Quick Start

### Prerequisites

- Docker and Docker Compose installed
- Certificate file (`Zscaler_Root_CA.cer`) in parent directory (`ai_upskilling/`)

### Running with Docker Compose

**Using Make (Recommended):**
```bash
# From the app/ directory
cd app
make compose-up-build
```

**Or manually:**
```bash
# From the task2-db-app directory
docker-compose up --build
```

This will:
1. Start PostgreSQL container
2. Build and start Flask app container
3. Initialize database tables (ready for PowerPoint uploads)
4. Make app available at http://localhost:5000

### Accessing the Application

- **Home**: http://localhost:5000
- **Database UI**: http://localhost:5000/db
- **Health Check**: http://localhost:5000/api/health
- **API - List Tables**: http://localhost:5000/db/tables
- **API - List Files**: http://localhost:5000/db/files
- **API - Get Table Data**: http://localhost:5000/db/table/presentation_slides
- **API - Get Table Data**: http://localhost:5000/db/table/slide_urls

### Stopping the Containers

**Using Make:**
```bash
make compose-down          # Stop containers
make compose-down-volumes  # Stop and clear database
```

**Or manually:**
```bash
docker-compose down        # Stop containers
docker-compose down -v     # Stop and clear database
```

### Other Useful Commands

```bash
make compose-logs          # View all logs
make compose-logs-app      # View app logs only
make compose-logs-db       # View database logs only
make compose-ps            # Show container status
make compose-restart       # Restart containers
make compose-shell-app     # Open shell in app container
make compose-shell-db      # Open PostgreSQL shell
```

## Database Tables

The application manages PowerPoint presentation data through the following tables:

### Presentation Files Table
- `id` - Primary key
- `filename` - Sanitized filename
- `original_filename` - Original uploaded filename
- `uploaded_at` - Upload timestamp
- `slide_count` - Number of slides extracted
- `url_count` - Number of URLs extracted

### Presentation Slides Table
- `id` - Primary key
- `slide_number` - Slide number in presentation
- `text` - Extracted text content
- `source_file` - Source filename (backward compatibility)
- `file_id` - Foreign key to presentation_files
- `created_at` - Timestamp

### Slide URLs Table
- `id` - Primary key
- `slide_id` - Foreign key to presentation_slides
- `url` - Extracted URL (HTTP/HTTPS/mailto)
- `link_text` - Associated link text
- `created_at` - Timestamp

## Project Structure

```
task2-db-app/
├── docker-compose.yml      # Multi-container orchestration
├── app/
│   ├── app.py             # Main Flask application
│   ├── models/            # Database models
│   │   ├── database.py   # DB initialization
│   │   └── tables.py     # Table models (PresentationFile, PresentationSlide, SlideUrl)
│   ├── routes/            # API routes
│   │   ├── api.py        # General API endpoints
│   │   └── database.py   # Database UI routes
│   ├── templates/         # HTML templates
│   │   ├── index.html    # Home page
│   │   ├── database.html # Database viewer with upload UI
│   │   └── upload.html   # Upload page (legacy)
│   ├── utils/            # Utility functions
│   │   └── pptx_parser.py # PowerPoint parsing logic
│   ├── static/            # Static files (CSS, JS)
│   ├── scripts/           # Utility scripts
│   │   ├── init_db.py    # Database initialization
│   │   └── debug_hyperlinks.py # Debug script for PowerPoint parsing
│   └── Dockerfile         # App container definition
└── README.md              # This file
```

## Environment Variables

Create a `.env` file in the root directory (optional):

```env
DB_USER=flaskuser
DB_PASSWORD=flaskpass
DB_NAME=flaskdb
DB_PORT=5432
APP_PORT=5000
```

## Development

### Running Locally (without Docker)

1. **Start PostgreSQL** (using Docker or local installation):
   ```bash
   docker run -d --name postgres-dev \
     -e POSTGRES_USER=flaskuser \
     -e POSTGRES_PASSWORD=flaskpass \
     -e POSTGRES_DB=flaskdb \
     -p 5432:5432 \
     postgres:15-alpine
   ```

2. **Set up Python environment**:
   ```bash
   cd app
   make install
   ```

3. **Initialize database**:
   ```bash
   python scripts/init_db.py
   ```

4. **Run the app**:
   ```bash
   make run
   ```

## API Endpoints

### Database Endpoints

- `GET /db/tables` - List all available tables
- `GET /db/table/<table_name>` - Get all records from a table
- `GET /db/table/<table_name>/record/<id>` - Get a specific record
- `GET /db/files` - List all uploaded PowerPoint files
- `POST /db/upload` - Upload and parse a PowerPoint file
- `POST /db/clear` - Clear all presentation data
- `DELETE /db/files/<file_id>` - Delete a specific file and its data

### General Endpoints

- `GET /api/health` - Health check (includes database status)

## Troubleshooting

### Database Connection Issues

- Check that PostgreSQL container is running: `docker ps`
- Verify database credentials in `.env` or `docker-compose.yml`
- Check logs: `docker-compose logs db`

### App Not Starting

- Check logs: `docker-compose logs app`
- Verify database is healthy before app starts (healthcheck)
- Ensure certificate file is accessible

### No Data Showing

- Database may not be initialized. Check app logs for initialization messages
- Upload a PowerPoint file via the web UI at http://localhost:5000/db
- Manually run: `docker-compose exec app python scripts/init_db.py`

## Usage

### Uploading PowerPoint Files

1. Navigate to http://localhost:5000/db
2. Click "Choose File" and select one or more `.pptx` files
3. Click "Upload & Parse" to extract text and URLs
4. View the extracted data in the tables below

### Managing Files

- View all uploaded files in the "Uploaded Files" section
- Click on table cards to view slides and URLs
- Delete individual files using the "Delete" button
- Clear all data using "Clear All Data" button

### Viewing Data

- Click on "Presentation Slides" to see all extracted slides
- Click on "Slide URLs" to see all extracted URLs (all clickable!)
- URLs open in new tabs when clicked

## Next Steps

- Add search/filter functionality
- Export data to CSV/JSON
- Add authentication
- Implement slide preview/thumbnails
- Add data validation and error handling

