#!/bin/bash

# DevContainer setup script with mise (Dockerfileless approach)
# This script runs after the container is created and tools are installed via mise

set -e

echo "🚀 Starting DevContainer setup with mise (Dockerfileless)..."

# Activate mise for this script
eval "$(mise activate bash)"

# Add mise activation to shell profiles
echo 'eval "$(mise activate bash)"' >> ~/.bashrc
echo 'eval "$(mise activate zsh)"' >> ~/.zshrc

# Ensure proper PATH for mise tools
echo 'export PATH="$HOME/.local/share/mise/shims:$PATH"' >> ~/.bashrc
echo 'export PATH="$HOME/.local/share/mise/shims:$PATH"' >> ~/.zshrc

# Install pre-commit hooks
echo "📋 Setting up pre-commit hooks..."
if [ -f ".pre-commit-config.yaml" ]; then
    pre-commit install
    echo "✅ Pre-commit hooks installed"
else
    echo "ℹ️  No .pre-commit-config.yaml found, skipping pre-commit setup"
fi

# Setup Python backend
echo "🐍 Setting up Python backend..."
cd backend

# Install Python dependencies with uv
if [ -f "pyproject.toml" ]; then
    echo "📦 Installing Python dependencies with uv..."
    uv sync --all-extras
    echo "✅ Python dependencies installed"
else
    echo "⚠️  No pyproject.toml found in backend directory"
fi

cd ..

# Setup JavaScript frontend
echo "📦 Setting up JavaScript frontend..."
cd frontend

# Install Node.js dependencies
if [ -f "package.json" ]; then
    echo "📦 Installing Node.js dependencies..."
    
    # Use bun for package installation (managed by mise)
    echo "Using bun for package installation..."
    bun install
    
    echo "✅ JavaScript dependencies installed"
else
    echo "⚠️  No package.json found in frontend directory"
fi

cd ..

# Setup git configuration
echo "🔧 Configuring git..."
git config --global init.defaultBranch main
git config --global pull.rebase false
git config --global core.autocrlf input
git config --global core.filemode false

# Create useful aliases
echo "⚙️  Setting up development aliases..."
cat >> ~/.bashrc << 'EOF'

# Development aliases
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'
alias ..='cd ..'
alias ...='cd ../..'

# Python aliases
alias py='python'
alias pytest='python -m pytest'
alias lint-py='cd backend && uv run ruff check . && uv run ruff format --check . && uv run mypy src'
alias fix-py='cd backend && uv run ruff check --fix . && uv run ruff format .'
alias test-py='cd backend && uv run pytest'

# JavaScript aliases
alias lint-js='cd frontend && bun run lint:check && bun run format:check && bun run typecheck'
alias fix-js='cd frontend && bun run lint && bun run format'
alias test-js='cd frontend && bun run test'
alias dev-js='cd frontend && bun run dev'

# Git aliases
alias gs='git status'
alias ga='git add'
alias gc='git commit'
alias gp='git push'
alias gl='git log --oneline -10'

# Docker aliases
alias dps='docker ps'
alias dimg='docker images'
alias dprune='docker system prune -f'

# Mise aliases
alias ms='mise ls'
alias msi='mise install'
alias msu='mise use'

EOF

# Copy to zsh as well
cat >> ~/.zshrc << 'EOF'

# Development aliases
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'
alias ..='cd ..'
alias ...='cd ../..'

# Python aliases
alias py='python'
alias pytest='python -m pytest'
alias lint-py='cd backend && uv run ruff check . && uv run ruff format --check . && uv run mypy src'
alias fix-py='cd backend && uv run ruff check --fix . && uv run ruff format .'
alias test-py='cd backend && uv run pytest'

# JavaScript aliases
alias lint-js='cd frontend && bun run lint:check && bun run format:check && bun run typecheck'
alias fix-js='cd frontend && bun run lint && bun run format'
alias test-js='cd frontend && bun run test'
alias dev-js='cd frontend && bun run dev'

# Git aliases
alias gs='git status'
alias ga='git add'
alias gc='git commit'
alias gp='git push'
alias gl='git log --oneline -10'

# Docker aliases
alias dps='docker ps'
alias dimg='docker images'
alias dprune='docker system prune -f'

# Mise aliases
alias ms='mise ls'
alias msi='mise install'
alias msu='mise use'

EOF

# Create a startup message
cat > ~/.welcome << 'EOF'
🎉 Welcome to your AI-Safe Development Container with mise!

📂 Project Structure:
   📁 backend/     - Python backend (using Python 3.13.5)
   📁 frontend/    - JavaScript frontend (using Node.js 20.11.0, Bun 1.1.42)
   📁 .devcontainer/ - DevContainer configuration (Dockerfileless)

🛠️  Tool Versions (managed by mise):
   🐍 Python: 3.13.5
   📦 Node.js: 20.11.0
   🚀 Bun: 1.1.42

🔒 AI Safety Features:
   - Containerized execution environment
   - Unified tool versions across all environments
   - Safe AI code generation and testing
   - Isolated development sandbox

🛠️  Quick Commands:
   lint-py    - Check Python code quality
   fix-py     - Auto-fix Python code issues
   test-py    - Run Python tests
   
   lint-js    - Check JavaScript code quality  
   fix-js     - Auto-fix JavaScript code issues
   test-js    - Run JavaScript tests
   dev-js     - Start frontend development server

💡 Tips:
   - All tools are managed by mise (run 'mise ls' to see versions)
   - Environment is identical to CI/CD and local mise setup
   - Dependencies are pre-installed
   - Pre-commit hooks are configured
   - AI-generated code runs safely in this container
   - Use Ctrl+Shift+` to open terminal

Happy and safe coding! 🚀🔒
EOF

# Add welcome message to shell profiles
echo 'cat ~/.welcome' >> ~/.bashrc
echo 'cat ~/.welcome' >> ~/.zshrc

echo "✅ DevContainer setup completed successfully!"
echo "🎯 Ready for development with mise-managed tools!"