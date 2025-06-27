#!/bin/bash

# Post-start script
# This script runs every time the container starts

set -e

echo "🔄 Running post-start setup..."

# Ensure proper ownership of workspace
sudo chown -R vscode:vscode /workspace

# Check if dependencies are installed and install if missing
echo "🔍 Checking dependencies..."

# Check Python dependencies
if [ -f "backend/pyproject.toml" ] && [ ! -d "backend/.venv" ]; then
    echo "📦 Installing missing Python dependencies..."
    cd backend && uv sync --all-extras && cd ..
fi

# Check Node.js dependencies  
if [ -f "frontend/package.json" ] && [ ! -d "frontend/node_modules" ]; then
    echo "📦 Installing missing Node.js dependencies..."
    cd frontend && npm install && cd ..
fi

# Start background services if needed
echo "🚀 Starting development services..."

# Example: Start a background file watcher or development server
# Uncomment and modify as needed for your project

# cd frontend && npm run dev &
# cd backend && uvicorn main:app --reload --host 0.0.0.0 --port 8000 &

echo "✅ Post-start setup completed!"
echo "🎯 Development environment is ready!"