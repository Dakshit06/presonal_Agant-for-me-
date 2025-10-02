#!/bin/bash

# Agentice Startup Script
echo "🚀 Starting Agentice Personal AI Assistant..."

# Activate virtual environment
source /workspaces/presonal_Agant-for-me-/.venv/bin/activate

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Using default configuration."
fi

# Kill any existing uvicorn processes
pkill -f uvicorn 2>/dev/null || true

# Start the server
echo "📡 Starting server on http://localhost:8000"
echo "📊 Dashboard: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo "💚 Health Check: http://localhost:8000/health"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
