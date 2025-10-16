#!/bin/bash
# Quick activation script for the virtual environment
# Usage: source activate.sh

echo "Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"
echo ""
echo "Available commands:"
echo "  python generate_initial_links.py      - Generate Session 1 URLs"
echo "  python app.py                          - Start Flask server"
echo "  python regenerate_links.py <file.xlsx> - Generate Session 2 URLs"
echo ""
