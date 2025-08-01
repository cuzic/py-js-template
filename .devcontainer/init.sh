#!/bin/bash

# DevContainer initialization script
# This script installs mise and prepares the environment

set -e

echo "🔧 Installing mise..."

# Set up for vscode user (since script may run as root)
VSCODE_HOME="/home/vscode"

# Ensure proper ownership of home directory
chown -R vscode:vscode $VSCODE_HOME

# Create necessary directories as vscode user
sudo -u vscode mkdir -p $VSCODE_HOME/.local/{bin,share}
sudo -u vscode chmod 755 $VSCODE_HOME/.local $VSCODE_HOME/.local/bin $VSCODE_HOME/.local/share

# Install mise as vscode user
sudo -u vscode bash -c 'curl -fsSL https://mise.jdx.dev/install.sh | sh'

# Add mise activation to shell profiles as vscode user
if ! sudo -u vscode grep -q "mise activate bash" $VSCODE_HOME/.bashrc; then
    sudo -u vscode bash -c 'echo '\''eval "$(~/.local/bin/mise activate bash)"'\'' >> ~/.bashrc'
fi

if ! sudo -u vscode grep -q "mise activate zsh" $VSCODE_HOME/.zshrc; then
    sudo -u vscode bash -c 'echo '\''eval "$(~/.local/bin/mise activate zsh)"'\'' >> ~/.zshrc'
fi

# Make scripts executable
chmod +x .devcontainer/*.sh

echo "✅ Mise installation completed!"
echo "🎯 Ready for setup on next start!"