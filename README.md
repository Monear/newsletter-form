# Student Writing Assignment System

A simple system for managing 2-session writing assignments using Microsoft Forms with student code-based access.

## Overview

Students complete a ~250 word writing assignment + upload 1 picture across two class sessions. This system uses Microsoft Forms for data collection with Python scripts to enable continuity between sessions.

## Features

- Student code-based access (no login required)
- Prefilled Microsoft Forms for seamless session continuity
- Automatic detection of picture uploads
- Simple Flask redirect server for local network access
- Works offline on local network

## System Requirements

- Python 3.8+
- Flask
- pandas
- openpyxl (for reading Excel files)

## Installation

```bash
pip install flask pandas openpyxl
```

## Quick Start

### 1. Create Your Microsoft Form

Create a form with these fields:
- **Student Name** (short text)
- **Writing Prompt** (long text, read-only/informational)
- **Your Writing** (long text)
- **Picture Status** (short text, optional - used in Session 2)
- **Upload Picture** (file upload)

### 2. Discover Form Field IDs

1. In Microsoft Forms, click "..." → "Get pre-filled URL"
2. Fill in sample data for each field
3. Click "Get pre-filled link"
4. Copy the URL and extract field parameter names (e.g., `entry.123456`)
5. Update `config.py` with these field IDs

### 3. Prepare Student List

Create `students.csv`:
```csv
code,name
STU001,John Doe
STU002,Jane Smith
STU003,Bob Johnson
```

### 4. Generate Initial Links

```bash
python generate_initial_links.py
```

This creates prefilled URLs for each student.

### 5. Start the Redirect Server

```bash
python app.py
```

Students can now visit `http://your-pc-ip:5000` and enter their code.

### 6. Between Sessions

After Session 1:
1. Download `responses.xlsx` from Microsoft Forms
2. Run: `python regenerate_links.py responses.xlsx`
3. Restart Flask app (or it auto-reloads)

Students entering their code in Session 2 will see their previous writing prefilled.

## File Structure

```
newsletter-form/
├── README.md                    # This file
├── config.py                    # Form configuration (field IDs)
├── generate_initial_links.py   # Creates initial prefilled URLs
├── regenerate_links.py          # Updates URLs with Session 1 responses
├── app.py                       # Flask redirect server
├── students.csv                 # Student codes and names
├── data/                        # Created automatically
│   └── responses.xlsx           # Downloaded from Forms
└── requirements.txt             # Python dependencies
```

## Workflow

### Session 1
1. Students visit redirect app and enter their code
2. Redirected to prefilled Form (name + prompt)
3. Write ~250 words
4. Upload picture
5. Submit

### Between Sessions
1. Download responses from Microsoft Forms
2. Run `regenerate_links.py` to update URLs
3. Flask app automatically picks up new URLs

### Session 2
1. Students enter same code
2. Redirected to NEW prefilled Form with:
   - Their Session 1 writing
   - Picture status message ("Already uploaded" or "Please upload")
3. Continue writing
4. Submit final version

## Troubleshooting

### URLs Too Long
If 250 words creates URLs that are too long:
- Reduce to 200 words
- Or split into multiple text fields

### Picture Not Detected
Check that the Excel column for picture uploads is not empty. The script checks for non-empty values in the picture column.

### Student Code Not Found
Ensure the code is spelled exactly as in `students.csv` (case-insensitive matching is enabled).

## Security Notes

- This system is designed for local network use only
- No authentication beyond student codes
- Ensure your PC firewall allows connections on port 5000
- Student data is stored in Microsoft Forms (follows your school's data policies)

## License

MIT License - Feel free to modify for your needs.
