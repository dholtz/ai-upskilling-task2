# Running the Flask App Locally

## Quick Start

### Option 1: Using the Run Script (Easiest)

```bash
cd app
./run_local.sh
```

This script will:
- Create a virtual environment if it doesn't exist
- Install dependencies automatically
- Start the Flask app

### Option 2: Manual Setup

#### Step 1: Navigate to the app directory
```bash
cd app
```

#### Step 2: Create and activate virtual environment
```bash
# Create virtual environment
python3 -m venv venv

# Activate it (macOS/Linux)
source venv/bin/activate

# On Windows:
# venv\Scripts\activate
```

#### Step 3: Install dependencies
```bash
pip install -r requirements.txt
```

#### Step 4: Run the app
```bash
python app.py
```

Or using Flask CLI:
```bash
flask run
```

## Testing the App

Once the app is running, you should see:
```
INFO:__main__:Starting Flask app on port 5000
 * Running on http://0.0.0.0:5000
```

### Test Endpoints

#### Option 1: Using the test script (in another terminal)
```bash
cd app
./test_endpoints.sh
```

#### Option 2: Manual testing with curl

**Root endpoint:**
```bash
curl http://localhost:5000/
```

**Health check:**
```bash
curl http://localhost:5000/api/health
```

**Example GET:**
```bash
curl http://localhost:5000/api/example
```

**Example POST:**
```bash
curl -X POST http://localhost:5000/api/example \
  -H "Content-Type: application/json" \
  -d '{"test": "data"}'
```

#### Option 3: Using a browser

Open these URLs in your browser:
- http://localhost:5000
- http://localhost:5000/api/health
- http://localhost:5000/api/example

#### Option 4: Using Python requests

```python
import requests

# Test root
response = requests.get('http://localhost:5000/')
print(response.json())

# Test health
response = requests.get('http://localhost:5000/api/health')
print(response.json())

# Test example POST
response = requests.post('http://localhost:5000/api/example', 
                        json={'test': 'data'})
print(response.json())
```

## Expected Responses

### GET /
```json
{
  "message": "Welcome to AI Up-Skilling Flask App",
  "version": "1.0.0",
  "endpoints": {
    "health": "/api/health",
    "example": "/api/example"
  },
  "documentation": "See README.md for usage instructions"
}
```

### GET /api/health
```json
{
  "status": "healthy",
  "service": "flask-app"
}
```

### GET /api/example
```json
{
  "message": "This is an example endpoint",
  "usage": "Add your AI/ML functionality here",
  "methods": ["GET", "POST"]
}
```

### POST /api/example
```json
{
  "message": "Received data",
  "data": {
    "test": "data"
  },
  "note": "This is where you'd process data with AI/ML models"
}
```

## Troubleshooting

### Port already in use
If port 5000 is already in use:
```bash
# Set a different port
export PORT=8080
python app.py
```

Or modify `.flaskenv` or create `.env`:
```
PORT=8080
```

### Import errors
Make sure you're in the `app` directory and the virtual environment is activated:
```bash
cd app
source venv/bin/activate
python app.py
```

### Module not found
Reinstall dependencies:
```bash
pip install -r requirements.txt
```

## Stopping the App

Press `Ctrl+C` in the terminal where the app is running.

