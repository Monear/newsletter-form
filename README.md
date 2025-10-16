# Student Writing Assignment System

A simple system for managing two-session writing assignments using Microsoft Forms with automatic student code-based access.

## What It Does

Students complete a ~250 word writing assignment across two class sessions. The system:
- Gives each student a personalized Microsoft Form
- Remembers their work between sessions
- Provides automatic word count feedback
- Works on your local network (no cloud setup needed)

## Quick Start

1. **For Non-Technical Users**: See [INSTRUCTIONS.md](INSTRUCTIONS.md)
2. **For Detailed Setup**: See [docs/SETUP.md](docs/SETUP.md)

## Features

- **No Student Login** - Students just enter their code (e.g., STU001)
- **Session Continuity** - Session 1 writing automatically carries over to Session 2
- **Word Count Feedback** - Automatic guidance to add/reduce words or confirm good length
- **UTF-8 Support** - Works with Vietnamese names and other special characters
- **Local Network** - Runs on your computer, students access via local network
- **Simple Interface** - Web-based entry, redirects to Microsoft Forms

## How It Works

### Session 1
1. Students visit your server (e.g., `http://192.168.1.100:5001`)
2. Enter their student code
3. Redirected to their personalized Microsoft Form
4. Write ~250 words
5. Submit

### Between Sessions
1. Download responses from Microsoft Forms
2. Run regeneration script
3. Server automatically updates with new URLs

### Session 2
1. Students use same code
2. See their Session 1 writing prefilled
3. Get feedback: "Add 50 more words" or "Good length" etc.
4. Continue writing and submit final version

## Requirements

- Python 3.8+ (tested with Python 3.13)
- Microsoft Forms account
- Local network for student access
- Computer to run the server during class

## Project Structure

```
newsletter-form/
├── students.xlsx          # Your student list (edit this)
├── results.xlsx           # Place Forms exports here
├── INSTRUCTIONS.md        # Quick start guide
├── README.md              # This file
├── src/                   # Source code (don't need to edit)
└── docs/                  # Detailed documentation
    └── SETUP.md          # Complete setup guide
```

## Installation

```bash
# Create virtual environment
python3 -m venv venv
source activate.sh

# Install dependencies
pip install -r requirements.txt

# Follow setup guide
open docs/SETUP.md
```

## Basic Workflow

**First Time Setup:**
```bash
# 1. Configure your Microsoft Form
python src/utils/extract_form_fields.py

# 2. Add students to students.xlsx
# 3. Generate Session 1 URLs
python src/generate_initial_links.py

# 4. Start server
python src/app.py
```

**After Session 1:**
```bash
# 1. Download results.xlsx from Microsoft Forms
# 2. Generate Session 2 URLs
python src/regenerate_links.py results.xlsx

# 3. Restart server (or visit /reload)
python src/app.py
```

## Documentation

- **Instructions.docx** - User-friendly Word document (generate with `python src/utils/md_to_docx.py INSTRUCTIONS.md`)
- **[INSTRUCTIONS.md](INSTRUCTIONS.md)** - Simple quick start for teachers
- **[docs/SETUP.md](docs/SETUP.md)** - Complete technical setup guide

## Troubleshooting

### Common Issues

**Port 5000 in use**: System uses port 5001 (macOS AirPlay uses 5000)

**Form doesn't load**: Check that generated URLs use `&` not `?` for parameters

**Students can't connect**: Verify firewall allows port 5001

**Vietnamese names broken**: Ensure students.xlsx saved with UTF-8 encoding

See [docs/SETUP.md](docs/SETUP.md) for detailed troubleshooting.

## Technical Details

- **Backend**: Flask (Python web framework)
- **Data**: Excel files (.xlsx) via pandas
- **Forms**: Microsoft Forms native prefill feature
- **Encoding**: UTF-8 with proper URL encoding (%20 for spaces)

## Security

Designed for local network use only:
- Student codes provide basic access control
- No authentication system
- Student data stored in Microsoft Forms
- Suitable for classroom environments

## License

MIT License - feel free to modify for your needs.

## Credits

Built for educational purposes using Microsoft Forms, Flask, and pandas.
