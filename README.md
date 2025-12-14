# Task 2: Database App

Flask application with PostgreSQL database integration. This project demonstrates deploying two containers (APP and DB) with a web UI to view database tables and records.

## Features

- ✅ **PostgreSQL Database** - Containerized PostgreSQL 15
- ✅ **Flask Application** - Containerized Flask app with database integration
- ✅ **Web UI** - Interactive interface to view tables and records
- ✅ **Docker Compose** - Multi-container orchestration
- ✅ **Sample Data** - Pre-populated with users and products tables

## Quick Start

### Prerequisites

- Docker and Docker Compose installed
- Certificate file (`Zscaler_Root_CA.cer`) in parent directory (`ai_upskilling/`)

### Running with Docker Compose

```bash
# From the task2-db-app directory
docker-compose up --build
```

This will:
1. Start PostgreSQL container
2. Build and start Flask app container
3. Initialize database with sample data
4. Make app available at http://localhost:5000

### Accessing the Application

- **Home**: http://localhost:5000
- **Database UI**: http://localhost:5000/db
- **Health Check**: http://localhost:5000/api/health
- **API - List Tables**: http://localhost:5000/db/tables
- **API - Get Table Data**: http://localhost:5000/db/table/users
- **API - Get Table Data**: http://localhost:5000/db/table/products

### Stopping the Containers

```bash
docker-compose down
```

To also remove the database volume (clears all data):
```bash
docker-compose down -v
```

## Database Tables

The application includes two tables with sample data:

### Users Table
- `id` - Primary key
- `username` - Unique username
- `email` - Unique email address
- `created_at` - Timestamp

### Products Table
- `id` - Primary key
- `name` - Product name
- `description` - Product description
- `price` - Product price (decimal)
- `stock` - Stock quantity
- `created_at` - Timestamp

## Project Structure

```
task2-db-app/
├── docker-compose.yml      # Multi-container orchestration
├── app/
│   ├── app.py             # Main Flask application
│   ├── models/            # Database models
│   │   ├── database.py   # DB initialization
│   │   └── tables.py     # Table models (User, Product)
│   ├── routes/            # API routes
│   │   ├── api.py        # General API endpoints
│   │   └── database.py   # Database UI routes
│   ├── templates/         # HTML templates
│   │   ├── index.html    # Home page
│   │   └── database.html # Database viewer
│   ├── static/            # Static files (CSS, JS)
│   ├── scripts/           # Utility scripts
│   │   └── init_db.py    # Database initialization
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

### General Endpoints

- `GET /api/health` - Health check (includes database status)
- `GET /api/example` - Example endpoint

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
- Manually run: `docker-compose exec app python scripts/init_db.py`

## Next Steps

- Add more tables
- Implement CRUD operations (Create, Read, Update, Delete)
- Add authentication
- Add data validation
- Implement search/filter functionality

