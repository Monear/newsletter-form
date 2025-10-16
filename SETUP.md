# Setup Guide

Complete step-by-step guide to setting up the Student Writing Assignment System.

## Part 1: Microsoft Forms Setup (15 minutes)

### Step 1: Create Your Form

1. Go to [Microsoft Forms](https://forms.office.com)
2. Click "New Form"
3. Give it a title: "Writing Assignment - Session 1"

### Step 2: Add Form Fields

Add the following fields in this exact order:

**Section 1: Student Information**

**Field 1: Student Code**
- Type: Text (short answer)
- Question: "Student Code"
- Description: "Your assigned code (e.g., STU001)"
- Required: Yes

**Field 2: Student Name**
- Type: Text (short answer)
- Question: "Student Name"
- Required: Yes

**Section 2: Writing Assignment**

**Field 3: Writing Prompt (Optional)**
- Type: Text (long answer)
- Question: "Your Writing Prompt"
- Description: This will show students their assignment
- Required: No (this is just informational)

**Field 4: Your Writing**
- Type: Text (long answer)
- Question: "Your Writing"
- Description: "Write about 250 words"
- Required: Yes

**Field 5: Progress from Session 1 (For Session 2 only)**
- Type: Text (long answer)
- Question: "Progress from Session 1"
- Description: "Your progress and feedback"
- Required: No

**Field 6: Upload Picture**
- Type: File upload
- Question: "Upload Picture"
- Required: Yes
- Settings: Allow one file, any image type

### Step 3: Discover Field IDs

This is the **most important step**!

1. In your form, click the "..." menu (top right)
2. Select "Get pre-filled URL"
3. Fill in ALL fields with sample data:
   - Student Code: "STU001"
   - Student Name: "Test Student"
   - Writing Prompt: "Sample prompt"
   - Your Writing: "Sample writing text here"
   - Progress from Session 1: "Test progress"
   - Skip the file upload
4. Click "Get pre-filled link"
5. Copy the URL - it will look like:
   ```
   https://forms.office.com/r/abc123xyz?entry.111=STU001&entry.222=Test+Student&entry.333=Sample+prompt&entry.444=Sample+writing+text+here&entry.555=Test+progress
   ```

6. Parse the URL to extract:
   - **Base URL**: Everything before the `?`
     - Example: `https://forms.office.com/r/abc123xyz`
   - **Field IDs**: The `entry.XXXXXX` parts
     - Student Code ID: `entry.111`
     - Student Name ID: `entry.222`
     - Writing Prompt ID: `entry.333`
     - Your Writing ID: `entry.444`
     - Progress Message ID: `entry.555`

### Step 4: Update config.py

Open `config.py` and update these values with your actual IDs:

```python
# Your values from the prefilled URL
BASE_FORM_URL = "https://forms.office.com/r/abc123xyz"
FIELD_STUDENT_CODE = "entry.111"
FIELD_STUDENT_NAME = "entry.222"
FIELD_WRITING_PROMPT = "entry.333"
FIELD_WRITING = "entry.444"
FIELD_PROGRESS_MESSAGE = "entry.555"
```

### Step 5: Update Excel Column Names

When you export responses from Forms, it creates an Excel file. Update these column names in `config.py` to match your form field names:

```python
EXCEL_COL_CODE = "Student Code"  # Must match Field 1 name
EXCEL_COL_NAME = "Student Name"  # Must match Field 2 name
EXCEL_COL_WRITING = "Your Writing"  # Must match Field 4 name
EXCEL_COL_PICTURE = "Upload Picture"  # Must match Field 6 name
```

**Important**: These must match EXACTLY as they appear in the Excel export (including capitalization and spaces).

## Part 2: Python Setup (10 minutes)

### Step 1: Install Dependencies

```bash
cd /Users/tyler/Desktop/newsletter-form
pip install -r requirements.txt
```

### Step 2: Prepare Student List

Edit `students.csv` with your actual student data:

```csv
code,name
STU001,John Doe
STU002,Jane Smith
STU003,Bob Johnson
```

**Tips:**
- Use simple codes (STU001, STU002, etc.)
- Students will enter their code in the form - the form will verify it matches
- Names are for reference only
- Add as many students as needed

### Step 3: Generate Initial Links

```bash
python generate_initial_links.py
```

This will:
- Validate your config.py setup
- Generate prefilled URLs for each student
- Update students.csv with URL column

**Expected output:**
```
Generating prefilled URLs for 25 students...

  STU001: John Doe
    → https://forms.office.com/r/abc123?entry.123=John+Doe...

✓ Successfully generated 25 prefilled URLs
✓ Updated students.csv with URLs
```

### Step 4: Test the System

Start the Flask server:

```bash
python app.py
```

**Expected output:**
```
============================================================
Student Writing Portal - Server Starting
============================================================

Students registered: 25

Server will start on: http://0.0.0.0:5000
...
```

### Step 5: Test Student Access

1. Open a browser
2. Go to `http://localhost:5000`
3. Enter a test code (e.g., "STU001")
4. You should be redirected to your Microsoft Form with:
   - Student code prefilled (STU001)
   - Student name prefilled (John Doe)
5. If it works, you're ready!

## Part 3: Deployment (5 minutes)

### Option A: Local Network (Recommended)

1. Find your computer's local IP address:
   - Mac: System Preferences → Network → Look for "IP Address"
   - Windows: `ipconfig` in Command Prompt
   - Linux: `ip addr` or `ifconfig`

2. Make sure your firewall allows connections on port 5000

3. Students can access via: `http://YOUR_IP:5000`
   - Example: `http://192.168.1.100:5000`

4. For easier access, create a shortened URL:
   - Use a URL shortener (bit.ly, TinyURL)
   - Or set up a local DNS entry
   - Or print QR codes (but you said labs can't scan)

### Option B: Always-On Server

If you want the system to run continuously:

**Mac/Linux:**
```bash
# Keep it running in background
nohup python app.py > server.log 2>&1 &
```

**Windows:**
- Use Windows Task Scheduler to run on startup
- Or use a tool like `pythonw.exe app.py`

## Part 4: Between-Session Workflow

After Session 1, follow these steps:

### Step 1: Download Responses

1. Open your Microsoft Form
2. Go to "Responses" tab
3. Click "Open in Excel" or click the Excel icon
4. Save the file as `responses.xlsx` in the project folder

### Step 2: Regenerate URLs

```bash
python regenerate_links.py responses.xlsx
```

**Expected output:**
```
Loading student data from students.csv...
  Found 25 students

Reading responses from responses.xlsx...
  Found 23 responses

Processing responses and generating new URLs...

  STU001: John Doe
    Words: 247 | Picture: ✓
    Status: Good length
    URL: 1456 characters

  STU002: Jane Smith
    Words: 198 | Picture: ⚠
    Status: Needs more words
    URL: 1302 characters

...

============================================================
Summary
============================================================
✓ Successfully regenerated URLs for 23 students

⚠ 2 students have NOT submitted yet:
  - STU015 (Alice Brown)
  - STU022 (Charlie Wilson)
```

### Step 3: Reload Flask Server

Either:

**Option A**: Restart the server
```bash
# Press Ctrl+C to stop
python app.py  # Start again
```

**Option B**: Visit reload URL
- Go to `http://YOUR_IP:5000/reload`
- This reloads the student mappings without restarting

### Step 4: Session 2 Ready!

Students can now enter their codes and will see:
- Their code and name (prefilled, confirms it's their form)
- Their Session 1 writing (prefilled)
- Progress message with:
  - Picture upload status
  - Word count from Session 1
  - Simple feedback (add more words, shorten, or good length)
- Ability to continue writing and submit final version

## Troubleshooting

### "Configuration incomplete" Error

**Problem**: Field IDs not set in config.py

**Solution**:
1. Follow Step 3 of Part 1 carefully
2. Make sure you copied the ENTIRE prefilled URL
3. Extract the exact `entry.XXXXXX` values

### "students.csv not found" Error

**Problem**: CSV file missing or in wrong location

**Solution**:
```bash
# Check you're in the right directory
pwd
# Should show: /Users/tyler/Desktop/newsletter-form

# Check file exists
ls students.csv
```

### "Column not found in Excel" Error

**Problem**: EXCEL_COL_* values in config.py don't match your Excel export

**Solution**:
1. Open `responses.xlsx` in Excel
2. Look at the column headers (first row)
3. Copy them EXACTLY to config.py
4. Watch for extra spaces or capitalization differences

### URLs Too Long

**Problem**: 250 words creates URLs over 2000 characters

**Solution**:
1. Test with actual student writing to see URL length
2. If needed, reduce word count to 200-220
3. Or split writing into two fields (Part 1 and Part 2)

### Student Codes Don't Match

**Problem**: Regenerate script can't find student code in responses

**Solution**:
- Ensure students entered their codes correctly (check responses.xlsx)
- Codes are case-insensitive (STU001 = stu001)
- Check that codes in students.csv match what students entered
- Fix any typos in either file

## Advanced Configuration

### Custom Writing Prompt

Edit `config.py`:

```python
WRITING_PROMPT = """
Your custom prompt here.

Can be multiple paragraphs.
"""
```

### Custom Word Count Ranges

Edit `config.py`:

```python
WORD_COUNT_TARGET = 250
WORD_COUNT_MIN = 240  # Below this: "add more words"
WORD_COUNT_MAX = 260  # Above this: "consider shortening"
```

### Change Server Port

Edit `config.py`:

```python
FLASK_PORT = 8080  # Change from 5000 to 8080
```

## Next Steps

✅ System is ready to use!

**Before Session 1:**
- Test with a few students
- Have backup plan (pen and paper) if tech fails
- Print the access URL on the board

**During Session 1:**
- Monitor the admin panel: `http://YOUR_IP:5000/admin`
- Help students who forget their codes

**Between Sessions:**
- Download responses and regenerate URLs
- Check which students haven't submitted

**Session 2:**
- Students use same codes
- They'll see their previous work
- Collect final submissions

## Support

If you run into issues:

1. Check the console output for error messages
2. Verify config.py is set up correctly
3. Test with a single student code first
4. Check that your Microsoft Form is still accessible

Good luck with your writing assignment!
