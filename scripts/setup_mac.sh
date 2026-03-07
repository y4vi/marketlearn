#!/usr/bin/env bash
set -euo pipefail

echo "Creating virtual environment .venv..."
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip

if ! command -v brew >/dev/null 2>&1; then
  echo "Homebrew not found. Please install Homebrew from https://brew.sh/ and re-run this script."
  exit 1
fi

echo "Installing TA-Lib via Homebrew..."
brew install ta-lib || true

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Setup complete. Activate the venv with: source .venv/bin/activate"
