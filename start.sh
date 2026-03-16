#!/usr/bin/env bash
# Start OpenStoryMode server

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
  echo "No .env file found. Let's set one up."
  echo ""
  read -rp "Enter your OpenRouter API key: " API_KEY
  if [ -z "$API_KEY" ]; then
    echo "Error: API key is required. Get one at https://openrouter.ai/"
    exit 1
  fi
  read -rp "Port (default 8000): " USER_PORT
  USER_PORT="${USER_PORT:-8000}"
  echo "OPENROUTER_API_KEY=$API_KEY" > .env
  echo "PORT=$USER_PORT" >> .env
  echo ""
  echo "Created .env file."
fi

# Create venv if it doesn't exist
if [ ! -d ".venv" ]; then
  echo "Creating virtual environment..."
  python3 -m venv .venv
  .venv/bin/pip install -r requirements.txt
fi

# Load port from .env or default to 8000
PORT="${PORT:-$(grep -s '^PORT=' .env | cut -d= -f2 || echo 8000)}"
PORT="${PORT:-8000}"

echo "Starting OpenStoryMode on http://localhost:$PORT"
exec .venv/bin/uvicorn app.main:app --host 0.0.0.0 --port "$PORT"
