# Quick Start Guide

This system helps students complete a two-session writing assignment using Microsoft Forms.

## For Teachers - Quick Steps

### Initial Setup (One Time)

1. **Add Your Students**
   - Open `students.xlsx` in Excel
   - Add student codes and names (columns: `code`, `name`)
   - Save the file

2. **Run the Setup Script**
   ```bash
   source activate.sh
   python src/generate_initial_links.py
   ```

3. **Start the Server**
   ```bash
   python src/app.py
   ```
   - Students visit the server on your local network
   - They enter their code and start writing

### After Session 1

1. **Download Student Responses**
   - Open your Microsoft Form
   - Click "Responses" tab
   - Click "Open in Excel"
   - Save as `results.xlsx` in this folder

2. **Generate Session 2 Links**
   ```bash
   python src/regenerate_links.py results.xlsx
   ```

3. **Restart the Server**
   - Press Ctrl+C to stop
   - Run `python src/app.py` again
   - Students enter their codes for Session 2

## Files You'll Work With

- **students.xlsx** - Your student list (you edit this)
- **results.xlsx** - Download from Microsoft Forms after each session
- **src/config.py** - Form configuration (usually set once during setup)

## Getting Help

If you need to reconfigure your Microsoft Form:
- Use `python src/utils/extract_form_fields.py` to extract field IDs
- Use `python src/utils/extract_excel_columns.py results.xlsx` to extract column names

For technical details, see `README.md` and `docs/SETUP.md`.
