#!/bin/bash
# Quick test script for API endpoints

BASE_URL="http://localhost:5000"

echo "Testing Flask App Endpoints"
echo "=========================="
echo ""

echo "1. Testing root endpoint (GET /):"
curl -s "$BASE_URL/" | python3 -m json.tool
echo ""
echo ""

echo "2. Testing health endpoint (GET /api/health):"
curl -s "$BASE_URL/api/health" | python3 -m json.tool
echo ""
echo ""

echo "3. Testing example endpoint (GET /api/example):"
curl -s "$BASE_URL/api/example" | python3 -m json.tool
echo ""
echo ""

echo "4. Testing example endpoint (POST /api/example):"
curl -s -X POST "$BASE_URL/api/example" \
  -H "Content-Type: application/json" \
  -d '{"test": "data", "message": "Hello from test script"}' | python3 -m json.tool
echo ""
echo ""

echo "All tests completed!"

