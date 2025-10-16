# Student Writing Assignment System - Instructions

A simple system for managing two-session writing assignments using Microsoft Forms.

## What This System Does

Your students complete a ~250 word writing assignment across two class sessions. The system:
- Gives each student their own personalized Microsoft Form
- Remembers their work between sessions automatically
- Provides feedback on word count ("add 50 more words" or "good length")
- Works on your classroom network (no internet setup needed)

## Quick Overview

### Session 1
1. Students visit a website on your computer (like `http://192.168.1.100:5001`)
2. They type in their student code
3. System opens their personal Microsoft Form
4. They write ~250 words
5. They click submit

### Between Sessions
1. You download the responses from Microsoft Forms (save as Excel file)
2. You run one command on your computer
3. System automatically updates with new links

### Session 2
1. Students use the same code as before
2. They see their Session 1 writing already filled in
3. They get feedback like "Add 50 more words" or "Good length - you can edit or submit"
4. They finish writing and submit

---

## Files You'll Use

When you open this folder, you'll see:

- **students.xlsx** - Your student list (you edit this in Excel)
- **results.xlsx** - Where you save the Forms responses after Session 1
- **Instructions.docx** - This guide as a Word document (easier to read)
- **src/** folder - The program files (you don't need to touch these)

---

## First Time Setup

### Step 1: Add Your Students

1. Open `students.xlsx` in Excel
2. Fill in the student codes and names:

| code   | name              | url |
|--------|-------------------|-----|
| STU001 | John Doe          |     |
| STU002 | Jane Smith        |     |
| STU003 | Bob Johnson       |     |

3. Leave the "url" column empty - the system fills this in automatically
4. Save the file

### Step 2: Configure Your Microsoft Form

If you haven't created your Microsoft Form yet, see the detailed setup guide in `docs/SETUP.md`.

If you have your Form ready:

1. Open Terminal (Mac) or Command Prompt (Windows)
2. Navigate to this folder
3. Run these commands:

```bash
source activate.sh
python src/utils/extract_form_fields.py
```

4. Paste your prefilled Forms URL when prompted
5. Type "yes" to update the configuration

### Step 3: Generate Student Links

Still in Terminal/Command Prompt:

```bash
python src/generate_initial_links.py
```

This creates a personalized link for each student. Check `students.xlsx` - the url column should now be filled in.

### Step 4: Start the Server

```bash
python src/app.py
```

You'll see a message like:
```
Server will start on: http://0.0.0.0:5001
```

**Keep this window open during class!**

### Step 5: Find Your Computer's Address

You need to tell students how to access your computer.

**On Mac:**
1. Click Apple menu → System Settings → Network
2. Look for "IP Address" (something like 192.168.1.100)

**On Windows:**
1. Open Command Prompt
2. Type `ipconfig`
3. Look for "IPv4 Address"

**Write this on the board:** `http://YOUR_IP:5001`

For example: `http://192.168.1.100:5001`

---

## Running Session 1

### Before Class

1. Make sure your computer is connected to the classroom network
2. Open Terminal and start the server:
   ```bash
   python src/app.py
   ```
3. Write the access URL on the board (like `http://192.168.1.100:5001`)

### During Class

1. Students open a web browser
2. They go to the URL on the board
3. They type their student code (like STU001)
4. They press "Start Writing"
5. Their Microsoft Form opens with their name already filled in
6. They complete the assignment (~250 words)
7. They click Submit

### Monitoring Students

While the server is running, you can check which students are registered:

Open a browser and go to: `http://YOUR_IP:5001/admin`

This shows all student codes and names.

---

## Between Sessions

### Step 1: Download Responses

1. Go to [Microsoft Forms](https://forms.office.com)
2. Open your form
3. Click the "Responses" tab at the top
4. Click "Open in Excel" (green Excel icon)
5. Excel will open with all the submissions
6. Save this file as `results.xlsx` in your project folder
7. Close Excel

### Step 2: Update the System

Open Terminal and run:

```bash
python src/regenerate_links.py results.xlsx
```

The system will:
- Read all the Session 1 submissions
- Count how many words each student wrote
- Create new links that include their previous writing
- Show you which students haven't submitted yet

You'll see output like:
```
✓ Successfully regenerated URLs for 25 students

⚠ 3 students have NOT submitted yet:
  - STU005 (Alice Brown)
  - STU012 (Charlie Wilson)
  - STU018 (David Lee)
```

### Step 3: Restart the Server

In the Terminal window where the server is running:
1. Press `Ctrl+C` to stop the server
2. Run `python src/app.py` again to restart

Or visit: `http://YOUR_IP:5001/reload` in your browser (faster, doesn't require restart)

---

## Running Session 2

The process is exactly the same as Session 1!

1. Start the server
2. Write the URL on the board
3. Students enter their codes

**The difference**: Students will now see:
- Their Session 1 writing already filled in
- A message showing their word count
- Feedback like:
  - "Session 1: 198 words written - Add about 52 more words to reach 250"
  - "Session 1: 247 words written - Good length - you can edit or submit"
  - "Session 1: 312 words written - Consider making it shorter by about 62 words"

They can edit their writing or add more, then submit the final version.

---

## Troubleshooting

### "Command not found" or "python: command not found"

**Solution**: You might need to use `python3` instead of `python`:

```bash
python3 src/app.py
```

### "Port 5001 already in use"

**Solution**: Another program is using that port. Either:
- Close other programs and try again
- Or ask someone technical to change the port in `src/config.py`

### Students can't access the server

**Check:**
1. Is the server still running? (Look for the Terminal window)
2. Are students on the same WiFi network as you?
3. Did you give them the correct IP address?
4. Is your firewall blocking connections? (May need IT help)

### Student forgot their code

**Solution**: Look it up in `students.xlsx` or visit `http://YOUR_IP:5001/admin` to see all codes.

### Form shows "This form doesn't exist"

**Solution**: The configuration might be wrong. Ask someone technical to check `docs/SETUP.md`.

### Need to add more students mid-session

1. Add them to `students.xlsx`
2. Run `python src/generate_initial_links.py`
3. Visit `http://YOUR_IP:5001/reload` or restart the server

---

## Tips for Success

**Before Session 1:**
- Test with 2-3 students first
- Make sure students can access from their devices
- Have a backup plan (pen and paper) if technology fails

**During Sessions:**
- Keep the Terminal window visible so you see if anything goes wrong
- Students can re-enter their code if they accidentally close the browser
- The same code works for both sessions

**Between Sessions:**
- Don't edit `students.xlsx` manually after generating links (unless adding new students)
- Keep the `results.xlsx` file in case you need to regenerate links

---

## Getting Help

**For more details:**
- See `README.md` for an overview
- See `docs/SETUP.md` for complete technical documentation

**Common tasks:**

**Reconfigure the Microsoft Form:**
```bash
python src/utils/extract_form_fields.py
```

**Update Excel column settings:**
```bash
python src/utils/extract_excel_columns.py results.xlsx
```

**Generate a Word version of this guide:**
```bash
python src/utils/md_to_docx.py INSTRUCTIONS.md
```
This creates `Instructions.docx` which is easier to read.

---

## Quick Command Reference

| Task | Command |
|------|---------|
| Activate environment | `source activate.sh` |
| Generate initial links | `python src/generate_initial_links.py` |
| Start server | `python src/app.py` |
| Regenerate links | `python src/regenerate_links.py results.xlsx` |
| Stop server | Press `Ctrl+C` in Terminal |

---

**Good luck with your writing assignment!**

For technical support, see `docs/SETUP.md` or contact your IT department.
