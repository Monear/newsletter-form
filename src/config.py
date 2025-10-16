"""
Configuration file for Microsoft Forms integration.

SETUP INSTRUCTIONS:
1. Create your Microsoft Form with the required fields
2. Use Forms UI to generate a pre-filled URL with sample data
3. Extract the field parameter names from the URL
4. Update the constants below with your actual values

Example URL structure:
https://forms.office.com/r/abc123?entry.12345=John&entry.67890=Sample+text

In this example:
- BASE_FORM_URL = "https://forms.office.com/r/abc123"
- FIELD_STUDENT_NAME = "entry.12345"
- FIELD_WRITING = "entry.67890"
"""

# ============================================================================
# FORM CONFIGURATION - UPDATE THESE VALUES
# ============================================================================

# Your Microsoft Form base URL (without parameters)
BASE_FORM_URL = "https://forms.office.com/Pages/ResponsePage.aspx?id=d1mqSFIaekWJPkWX4jID-6TR2-msV21DiHgXDnqmbZlUNEhVQU41QUYwM0FaOUo3N1pSTEU1M0dKSyQlQCN0PWcu"

# Field parameter names from the prefilled URL
# These are the parameter names in the URL query string
FIELD_STUDENT_NAME = "rd51cb215ea174739855916df02ad44cf"
FIELD_STUDENT_CODE = "rfaae22d4640947ab85996a667a073e61"
FIELD_WRITING_INFO = "r211ff00659f648f295754189f7d59c8e"  # Shows instructions in Session 1, progress in Session 2
FIELD_WRITING = "rf3225a2a947c4da49b18ae7daf8a1fa9"

# ============================================================================
# EXCEL COLUMN NAMES - Update based on your Forms export
# ============================================================================

# Column names in the Excel export from Microsoft Forms
EXCEL_COL_TIMESTAMP = "Start time"  # Or "Timestamp", depends on Forms export
EXCEL_COL_CODE = "Student Code"  # Must match your Form field name
EXCEL_COL_NAME = "Name1"  # Forms added "1" because there are multiple "Name" references
EXCEL_COL_WRITING = "Newsletter Content"  # Must match your Form field name

# ============================================================================
# ASSIGNMENT CONFIGURATION
# ============================================================================

# Session 1: Instructions shown in "Writing Info" field
WRITING_INFO_SESSION_1 = "By the end of this class you should write around 250 words."

# Word count target and ranges
WORD_COUNT_TARGET = 250
WORD_COUNT_MIN = 240  # Below this: suggest adding more
WORD_COUNT_MAX = 260  # Above this: suggest reducing

# ============================================================================
# SERVER CONFIGURATION
# ============================================================================

# Flask server settings
FLASK_HOST = "0.0.0.0"  # Allow connections from any device on local network
FLASK_PORT = 5001  # Changed from 5000 (conflicts with macOS AirPlay)
FLASK_DEBUG = True  # Set to False in production
