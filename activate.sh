#!/bin/bash
# Quick activation script for the virtual environment
# Usage: source activate.sh

echo "Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"
echo ""
echo "Available commands:"
echo "  python src/generate_initial_links.py      - Generate Session 1 URLs"
echo "  python src/app.py                          - Start Flask server"
echo "  python src/regenerate_links.py <file.xlsx> - Generate Session 2 URLs"
echo ""
echo "Utility scripts:"
echo "  python src/utils/extract_form_fields.py    - Extract form field IDs from URL"
echo "  python src/utils/extract_excel_columns.py  - Extract column names from Excel"
echo ""
