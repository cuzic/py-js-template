#!/bin/bash

# DevContainer post-start script
# This script runs every time the container starts

echo "🔄 DevContainer post-start setup..."

# Activate mise
eval "$(mise activate bash)"

# Show current tool versions
echo "📋 Current tool versions:"
echo "Python: $(mise exec -- python --version 2>/dev/null || echo 'Not installed')"
echo "Node.js: $(mise exec -- node --version 2>/dev/null || echo 'Not installed')"
echo "Bun: $(mise exec -- bun --version 2>/dev/null || echo 'Not installed')"

# Check if dependencies are installed
echo "🔍 Checking project dependencies..."

# Check Python dependencies
if [ -f "backend/pyproject.toml" ]; then
    cd backend
    if [ ! -d ".venv" ]; then
        echo "📦 Installing Python dependencies..."
        uv sync --all-extras
    else
        echo "✅ Python dependencies already installed"
    fi
    cd ..
fi

# Check JavaScript dependencies
if [ -f "frontend/package.json" ]; then
    cd frontend
    if [ ! -d "node_modules" ]; then
        echo "📦 Installing JavaScript dependencies..."
        bun install
    else
        echo "✅ JavaScript dependencies already installed"
    fi
    cd ..
fi

echo "✅ DevContainer is ready for development!"