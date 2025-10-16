# Student Writing Assignment System

A simple, professional system for managing 2-session writing assignments using Microsoft Forms with student code-based access.

## Overview

Students complete a ~250 word writing assignment across two class sessions. This system uses Microsoft Forms for data collection with Python scripts to enable continuity between sessions.

**Key Features:**
- Student code-based access (no login required)
- Prefilled Microsoft Forms for seamless session continuity
- Automatic word count feedback
- Simple Flask redirect server for local network access
- Works offline on local network
- UTF-8 support for international names

## Project Structure

```
newsletter-form/
├── students.xlsx              # Student list (edit this file)
├── results.xlsx               # Place Forms exports here
├── INSTRUCTIONS.md            # Quick start guide for non-technical users
├── README.md                  # This file (technical documentation)
├── requirements.txt           # Python dependencies
├── activate.sh                # Virtual environment activation helper
│
├── src/                       # Source code
│   ├── app.py                # Flask redirect server
│   ├── config.py             # Form configuration
│   ├── generate_initial_links.py   # Creates Session 1 URLs
│   ├── regenerate_links.py         # Creates Session 2 URLs
│   └── utils/                # Utility scripts
│       ├── extract_form_fields.py     # Extract field IDs from URL
│       └── extract_excel_columns.py   # Extract column names from Excel
│
├── docs/                      # Documentation
│   ├── SETUP.md              # Detailed setup instructions
│   └── EXAMPLE_MESSAGES.md   # Example feedback messages
│
└── venv/                      # Python virtual environment (auto-created)
```

## System Requirements

- Python 3.8+ (tested with Python 3.13)
- Microsoft Forms account
- Local network for student access

## Quick Start

For non-technical users, see **INSTRUCTIONS.md**.

For detailed setup, see **docs/SETUP.md**.

### Installation

1. **Create virtual environment:**
   ```bash
   python3 -m venv venv
   source activate.sh  # or: source venv/bin/activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Basic Workflow

**Session 1:**
1. Edit `students.xlsx` with your student list
2. Run `python src/generate_initial_links.py`
3. Start server: `python src/app.py`
4. Students visit http://YOUR_IP:5001 and enter their codes

**After Session 1:**
1. Download responses from Forms → save as `results.xlsx`
2. Run `python src/regenerate_links.py results.xlsx`
3. Restart server

**Session 2:**
- Students enter same codes
- See their Session 1 writing and word count feedback
- Continue or edit their work

## Configuration

### Initial Setup

1. **Create Microsoft Form** with 4 fields:
   - Student Name (short text)
   - Student Code (short text)
   - Newsletter Content (long text)
   - Info (short text) - dual purpose field

2. **Extract Field IDs:**
   ```bash
   python src/utils/extract_form_fields.py
   ```
   Follow prompts to paste your prefilled URL

3. **Extract Excel Columns** (after first submission):
   ```bash
   python src/utils/extract_excel_columns.py results.xlsx
   ```

Both utilities automatically update `src/config.py`.

## Server Endpoints

- `/` - Student entry page
- `/admin` - View registered students
- `/reload` - Reload student mappings from Excel

## Technical Details

### Word Count Feedback

The system provides gentle, constructive feedback:
- **< 240 words**: "Add about X more words to reach 250"
- **240-260 words**: "Good length - you can edit or submit"
- **> 260 words**: "Consider making it shorter by about X words"

### URL Encoding

- Uses `quote_via=quote` for proper `%20` space encoding (Microsoft Forms requirement)
- Base URL format: `https://forms.office.com/...?id=...` + `&field=value&...`

### Code Matching

- Student codes are case-insensitive
- Matching is code-based (not name-based) for reliability
- Handles UTF-8 characters in names

### Session Management

- Session 1: Instructions prefilled in "Info" field
- Session 2: Progress message prefilled showing word count and feedback

## Security Notes

- Designed for **local network use only**
- No authentication beyond student codes
- Ensure firewall allows connections on port 5001
- Student data stored in Microsoft Forms (follows your organization's policies)
- No sensitive data in this repository

## Troubleshooting

### Port 5000 Conflict
Port 5000 conflicts with macOS AirPlay. System uses port 5001 by default.

### Form Doesn't Load
Verify URL format in `config.py`:
- Base URL must end with `?id=...`
- Additional parameters use `&` not `?`

### Column Name Mismatch
Forms may append numbers to duplicate field names (e.g., "Name1").
Run `extract_excel_columns.py` to auto-detect correct names.

### URL Too Long
Microsoft Forms supports URLs up to ~2000 characters. With 250 words, this should not be an issue.

## Development

### Running Tests
```bash
source activate.sh
python src/generate_initial_links.py  # Test URL generation
python src/app.py  # Test server
```

### Making Changes
1. Edit code in `src/` directory
2. Test locally
3. Update documentation if needed
4. Commit changes

## License

MIT License - Feel free to modify for your needs.

## Credits

Built for educational purposes. Uses Microsoft Forms, Flask, and pandas.
