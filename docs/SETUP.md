# Complete Setup Guide

Comprehensive step-by-step guide for setting up the Student Writing Assignment System.

## Overview

This system enables students to complete a ~250-word writing assignment across two class sessions using Microsoft Forms with seamless continuity between sessions.

**Time Required**: 30 minutes for initial setup

---

## Part 1: Microsoft Forms Setup (15 minutes)

### Step 1: Create Your Form

1. Go to [Microsoft Forms](https://forms.office.com)
2. Click "New Form"
3. Give it a title: "Writing Assignment"

### Step 2: Add Form Fields

Add exactly **4 fields** in this order:

#### Field 1: Student Code
- **Type**: Text (short answer)
- **Question**: "Student Code"
- **Description**: "Your assigned code (e.g., STU001)"
- **Required**: Yes

#### Field 2: Student Name
- **Type**: Text (short answer)
- **Question**: "Name"
- **Required**: Yes

#### Field 3: Newsletter Content
- **Type**: Text (long answer)
- **Question**: "Newsletter Content"
- **Description**: "Write about 250 words"
- **Required**: Yes

#### Field 4: Info
- **Type**: Text (short answer)
- **Question**: "Info:"
- **Description**: "Instructions and progress feedback"
- **Required**: No
- **Note**: This dual-purpose field shows instructions in Session 1 and progress in Session 2

### Step 3: Get Prefilled URL

This is the **most important step**!

1. In your form, click the "..." menu (top right)
2. Select "Get pre-filled URL"
3. Fill in ALL fields with sample data:
   - **Student Code**: "STU001"
   - **Name**: "Test Student"
   - **Newsletter Content**: "This is sample writing text for testing the prefill feature."
   - **Info**: "By the end of this class you should write around 250 words."

4. Click "Get pre-filled link"
5. Copy the entire URL - it will look like:
   ```
   https://forms.office.com/Pages/ResponsePage.aspx?id=xxxxx
   &rfaae22d4640947ab85996a667a073e61=STU001
   &rd51cb215ea174739855916df02ad44cf=Test%20Student
   &rf3225a2a947c4da49b18ae7daf8a1fa9=This%20is%20sample%20writing...
   &r211ff00659f648f295754189f7d59c8e=By%20the%20end%20of%20this%20class...
   ```

### Step 4: Extract Field IDs (Automated)

Run the field extraction utility:

```bash
python src/utils/extract_form_fields.py
```

**What this does**:
1. Prompts you to paste your prefilled URL
2. Automatically parses the URL
3. Extracts the base URL and all field parameter IDs
4. Attempts to identify which field is which based on sample values
5. Updates `src/config.py` with the correct field mappings

**Expected Output**:
```
======================================================================
Microsoft Forms Field Extractor
======================================================================

Paste your prefilled Forms URL here:
[you paste URL]

Base URL: https://forms.office.com/Pages/ResponsePage.aspx?id=xxxxx

Found fields:

  rfaae22d4640947ab85996a667a073e61
    Sample value: 'STU001'

  rd51cb215ea174739855916df02ad44cf
    Sample value: 'Test Student'

  ...

✓ Successfully identified all 4 fields!

Update config.py with these values? (yes/no):
```

**After completion**: Open `src/config.py` and verify the field mappings are correct.

### Step 5: Extract Excel Column Names (After First Test Submission)

After you make a test submission and download the Excel export:

```bash
python src/utils/extract_excel_columns.py results.xlsx
```

**What this does**:
1. Reads your Excel file
2. Shows all column names
3. Auto-matches columns to config variables
4. Updates `src/config.py` with correct column names

**Important**: Microsoft Forms may append numbers to duplicate field names (e.g., "Name" becomes "Name1"). The utility handles this automatically.

---

## Part 2: Python Setup (10 minutes)

### Step 1: Install Dependencies

```bash
# Navigate to project directory
cd /path/to/newsletter-form

# Create virtual environment (first time only)
python3 -m venv venv

# Activate virtual environment
source activate.sh  # or: source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

**Dependencies**:
- Flask 3.0.0 - Web server
- pandas ≥2.2.0 - Excel file handling
- openpyxl ≥3.1.2 - Excel file format support

### Step 2: Prepare Student List

1. Open `students.xlsx` (or create from `students.xlsx.template`)
2. Add your student data:

| code   | name              | url |
|--------|-------------------|-----|
| STU001 | Nguyễn Thị Hương  |     |
| STU002 | Trần Văn Minh     |     |
| STU003 | Lê Thị Lan        |     |

**Important**:
- Leave the `url` column empty (it will be populated automatically)
- Use simple, memorable codes
- Student names support UTF-8 (Vietnamese, etc.)
- Codes are case-insensitive

### Step 3: Generate Initial Links

```bash
python src/generate_initial_links.py
```

**What this does**:
1. Validates your `src/config.py` setup
2. Reads `students.xlsx`
3. Generates a prefilled URL for each student
4. Updates `students.xlsx` with the generated URLs

**Expected Output**:
```
Generating prefilled URLs for 10 students...

  STU001: Nguyễn Thị Hương
    → https://forms.office.com/Pages/ResponsePage.aspx?id=...

  STU002: Trần Văn Minh
    → https://forms.office.com/Pages/ResponsePage.aspx?id=...

  ...

✓ Successfully generated 10 prefilled URLs
✓ Updated students.xlsx with URLs

Next steps:
  1. Start the Flask server: python src/app.py
  2. Students can access via: http://YOUR_IP:5001
  3. After Session 1, download responses and run: python src/regenerate_links.py results.xlsx
```

### Step 4: Test the System

Start the Flask server:

```bash
python src/app.py
```

**Expected Output**:
```
============================================================
Student Writing Portal - Server Starting
============================================================

Students registered: 10

Server will start on: http://0.0.0.0:5001

Access URLs:
  - Student entry: http://YOUR_IP:5001/
  - Admin panel:   http://YOUR_IP:5001/admin
  - Reload data:   http://YOUR_IP:5001/reload

Press Ctrl+C to stop the server
============================================================
```

### Step 5: Verify Student Access

1. Open a browser
2. Go to `http://localhost:5001`
3. Enter a test code (e.g., "STU001")
4. You should be redirected to Microsoft Forms with:
   - Student code prefilled: "STU001"
   - Student name prefilled: "Nguyễn Thị Hương"
   - Info field showing: "By the end of this class you should write around 250 words."
5. If successful, you're ready for Session 1!

---

## Part 3: Deployment (5 minutes)

### Find Your Local IP Address

**macOS**:
```bash
ifconfig | grep "inet " | grep -v 127.0.0.1
```

**Windows**:
```cmd
ipconfig
```
Look for "IPv4 Address"

**Linux**:
```bash
ip addr show | grep "inet "
```

### Configure Firewall

Ensure port 5001 is open on your firewall:

**macOS**:
- System Settings → Network → Firewall
- Allow incoming connections for Python

**Windows**:
- Windows Defender Firewall → Advanced Settings
- Inbound Rules → New Rule → Port 5001

### Student Access

Students access via: `http://YOUR_IP:5001`

**Example**: `http://192.168.1.100:5001`

**Tips**:
- Write the URL on the board
- Test from a student device before class
- Keep the server running during the session

---

## Part 4: Session 1 Workflow

### Before Class

1. Start Flask server: `python src/app.py`
2. Verify server is accessible from student devices
3. Have the access URL ready to share

### During Class

1. Students visit `http://YOUR_IP:5001`
2. They enter their student code
3. Redirected to their personalized Form
4. Complete writing assignment (~250 words)
5. Submit form

### Monitor Progress

Visit admin panel: `http://YOUR_IP:5001/admin`

Shows all students and their registration status.

---

## Part 5: Between Sessions Workflow

### Step 1: Download Responses

1. Open your Microsoft Form
2. Go to "Responses" tab
3. Click "Open in Excel" (Excel icon)
4. Save file as `results.xlsx` in project root

### Step 2: Regenerate URLs

```bash
python src/regenerate_links.py results.xlsx
```

**What this does**:
1. Loads student roster from `students.xlsx`
2. Reads Session 1 responses from `results.xlsx`
3. Matches responses to students by code
4. Calculates word count for each submission
5. Generates progress feedback messages
6. Creates new prefilled URLs with:
   - Previous writing included
   - Word count and feedback
7. Updates `students.xlsx` with new URLs

**Expected Output**:
```
Loading student data from students.xlsx...
  Found 10 students

Reading responses from results.xlsx...
  Found 8 responses

Processing responses and generating new URLs...

  STU002: Trần Văn Minh
    Words: 27
    Status: Needs more words
    URL: 596 characters

  STU005: Hoàng Thị Mai
    Words: 247
    Status: Good length
    URL: 1234 characters

  ...

============================================================
Summary
============================================================
✓ Successfully regenerated URLs for 8 students

⚠ 2 students have NOT submitted yet:
  - STU001 (Nguyễn Thị Hương)
  - STU003 (Lê Thị Lan)

Next steps:
  1. Restart Flask server (Ctrl+C then: python src/app.py)
     OR visit: http://YOUR_IP:5001/reload
  2. Students enter their codes for Session 2
  3. They will see:
     - Their writing from Session 1
     - Word count and feedback
```

### Step 3: Reload Server

**Option A**: Restart the server
```bash
# Press Ctrl+C to stop
python src/app.py  # Start again
```

**Option B**: Hot reload (no restart needed)
- Visit `http://YOUR_IP:5001/reload`
- Server reloads student mappings from `students.xlsx`

---

## Part 6: Session 2 Workflow

### Student Experience

1. Students visit same URL: `http://YOUR_IP:5001`
2. Enter same student code
3. Redirected to Form prefilled with:
   - Their name and code
   - **Their complete Session 1 writing**
   - **Progress feedback** showing:
     - Word count from Session 1
     - Guidance to add/reduce words or confirm good length

### Progress Message Examples

The "Info:" field will show different messages based on word count:

#### Perfect Length (240-260 words)
Student wrote 247 words:
```
Session 1: 247 words written
Good length - you can edit or submit
```

#### Needs More Words (< 240 words)
Student wrote 198 words:
```
Session 1: 198 words written
Add about 52 more words to reach 250
```

#### Too Many Words (> 260 words)
Student wrote 312 words:
```
Session 1: 312 words written
Consider making it shorter by about 62 words
```

### Word Count Configuration

Customize thresholds in `src/config.py`:

```python
WORD_COUNT_TARGET = 250  # Goal word count
WORD_COUNT_MIN = 240     # Below this: "add more words"
WORD_COUNT_MAX = 260     # Above this: "consider shortening"
```

Students between MIN and MAX see: "Good length - you can edit or submit"

### Customizing Messages

Edit the Session 1 instructions in `src/config.py`:

```python
WRITING_INFO_SESSION_1 = "By the end of this class you should write around 250 words."
```

To customize Session 2 feedback logic, edit `generate_progress_message()` in `src/regenerate_links.py`.

---

## Troubleshooting

### Configuration Errors

#### "Configuration incomplete"

**Problem**: Field IDs not set in `src/config.py`

**Solution**:
1. Verify you ran `extract_form_fields.py`
2. Check that `src/config.py` has values like:
   ```python
   FIELD_STUDENT_CODE = "rfaae22d4640947..."  # Long ID, not placeholder
   ```
3. If values look like `"entry.YOUR_CODE_FIELD_ID"`, re-run the extraction utility

#### "Column not found in Excel"

**Problem**: Excel column names don't match `src/config.py`

**Solution**:
1. Open `results.xlsx` in Excel
2. Check the exact column headers (first row)
3. Run `extract_excel_columns.py results.xlsx`
4. Verify `src/config.py` was updated with correct names

**Common Issue**: Forms appends "1" to duplicate names
- If you have multiple "Name" references, Forms may export as "Name1"
- The extraction utility handles this automatically

### File Errors

#### "students.xlsx not found"

**Problem**: Missing or incorrectly named file

**Solution**:
```bash
# Verify you're in project root
pwd  # Should show: /path/to/newsletter-form

# Check file exists
ls students.xlsx

# If missing, copy from template
cp students.xlsx.template students.xlsx
```

#### Permission errors reading/writing files

**Solution**: Ensure Excel files are not open in Excel when running scripts

### Network/Server Errors

#### Port 5001 already in use

**Problem**: Another process using port 5001

**Solution**:
```bash
# Find process using port
lsof -i :5001

# Kill the process or change port in src/config.py:
FLASK_PORT = 8080  # Use different port
```

#### Can't access from student devices

**Problem**: Firewall blocking connections

**Solution**:
1. Verify server is running
2. Check firewall settings (see Part 3)
3. Test from another device on same network
4. Ensure using correct IP address (not localhost)

### URL/Form Errors

#### "This form doesn't exist"

**Problem**: Incorrect URL format

**Solution**:
- Verify `BASE_FORM_URL` in config ends with `?id=...`
- Should NOT have additional `?` in generated URLs
- Check `generate_prefilled_url()` uses `&` to join parameters

#### Text shows "word+word+word" instead of "word word word"

**Problem**: Wrong space encoding

**Solution**: Verify `generate_prefilled_url()` uses:
```python
urlencode(params, quote_via=quote)  # Not just urlencode(params)
```

#### Vietnamese/special characters broken

**Problem**: UTF-8 encoding issue

**Solution**:
- Ensure `students.xlsx` saved with UTF-8 encoding
- Python 3 handles UTF-8 by default
- Verify names display correctly in admin panel

### Data Matching Errors

#### "Student code not found in students.xlsx"

**Problem**: Code mismatch between submission and roster

**Solution**:
1. Open `results.xlsx` and check codes students actually entered
2. Compare with codes in `students.xlsx`
3. Codes are case-insensitive (STU001 = stu001)
4. Fix any typos in either file
5. Re-run `regenerate_links.py`

#### Students see wrong prefilled data

**Problem**: Code collisions or data mismatch

**Solution**:
1. Verify student codes are unique in `students.xlsx`
2. Check admin panel for duplicate codes
3. Ensure latest `students.xlsx` loaded (visit `/reload`)

---

## Advanced Configuration

### Custom Server Port

Edit `src/config.py`:

```python
FLASK_PORT = 8080  # Change from 5001
```

Restart server for changes to take effect.

### Custom Word Count Targets

Edit `src/config.py`:

```python
WORD_COUNT_TARGET = 200  # Lower target
WORD_COUNT_MIN = 180
WORD_COUNT_MAX = 220
```

Changes apply to next `regenerate_links.py` run.

### Custom Session 1 Instructions

Edit `src/config.py`:

```python
WRITING_INFO_SESSION_1 = """
Write a newsletter about your week.

Include:
- What you learned
- What you enjoyed
- What challenged you

Aim for 200-250 words.
"""
```

Changes apply to next `generate_initial_links.py` run.

### Running Server in Background

**macOS/Linux**:
```bash
nohup python src/app.py > server.log 2>&1 &
```

**Stop background server**:
```bash
# Find process ID
ps aux | grep "python src/app.py"

# Kill process
kill <PID>
```

---

## Production Checklist

Before using with students:

- [ ] Test with multiple student codes
- [ ] Verify UTF-8 names display correctly
- [ ] Check Forms accessible from student devices
- [ ] Confirm server accessible on local network
- [ ] Test complete Session 1 → Session 2 workflow
- [ ] Have backup plan if system fails
- [ ] Print access URL large enough for students to see
- [ ] Test `/admin` panel for monitoring
- [ ] Verify firewall allows port 5001
- [ ] Ensure computer won't sleep during session

---

## Support & Next Steps

**For Non-Technical Users**: See `Instructions.docx` (Word document)
Generate with: `python src/utils/md_to_docx.py INSTRUCTIONS.md`

**For Quick Start**: See `INSTRUCTIONS.md`

**For Simple Overview**: See `README.md`

**For Technical Details**: Review source code in `src/`

**Common Questions**:

**Q: Can students access from home?**
A: Not by default. System designed for local network. Would need port forwarding or cloud deployment.

**Q: What if a student forgets their code?**
A: Check `/admin` panel or `students.xlsx` to look up by name.

**Q: Can I change word count target mid-session?**
A: Yes, edit `config.py` and re-run `regenerate_links.py`.

**Q: What happens to students who didn't submit Session 1?**
A: They see blank forms in Session 2 (same as Session 1 experience).

**Q: How do I add more students mid-session?**
A: Add to `students.xlsx`, run `generate_initial_links.py`, visit `/reload`.

**Good luck with your writing assignment!**
