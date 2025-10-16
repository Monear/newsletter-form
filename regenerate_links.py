#!/usr/bin/env python3
"""
Regenerate prefilled Microsoft Forms URLs with student responses from Session 1.

This script reads the Excel export from Microsoft Forms after Session 1,
extracts student responses, and generates new prefilled URLs for Session 2
that include their previous writing and picture upload status.

Usage:
    python regenerate_links.py responses.xlsx
"""

import csv
import sys
import pandas as pd
from urllib.parse import urlencode
import config
from generate_initial_links import generate_prefilled_url


def load_current_students():
    """Load current student mappings from students.csv."""
    students = {}

    try:
        with open('students.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                code = row['code'].strip().upper()
                students[code] = {
                    'name': row['name'].strip(),
                    'code': code
                }
    except FileNotFoundError:
        print("ERROR: students.csv not found!")
        print("This file should exist from initial setup.")
        sys.exit(1)

    return students


def generate_progress_message(word_count):
    """
    Generate a simple progress message for Session 2.

    Args:
        word_count: Number of words written in Session 1

    Returns:
        Progress message string
    """
    messages = []

    # Word count feedback
    messages.append(f"Session 1: {word_count} words written")

    if word_count < config.WORD_COUNT_MIN:
        needed = config.WORD_COUNT_TARGET - word_count
        messages.append(f"Add about {needed} more words to reach 250")
    elif word_count > config.WORD_COUNT_MAX:
        extra = word_count - config.WORD_COUNT_TARGET
        messages.append(f"Consider making it shorter by about {extra} words")
    else:
        messages.append("Good length - you can edit or submit")

    return "\n".join(messages)


def regenerate_links(excel_file):
    """
    Regenerate prefilled URLs with Session 1 responses.

    Args:
        excel_file: Path to Excel file exported from Microsoft Forms
    """

    # Load current student mappings
    print("Loading student data from students.csv...")
    students = load_current_students()
    print(f"  Found {len(students)} students")
    print()

    # Read Excel file
    print(f"Reading responses from {excel_file}...")
    try:
        df = pd.read_excel(excel_file)
    except FileNotFoundError:
        print(f"ERROR: File not found: {excel_file}")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR reading Excel file: {e}")
        sys.exit(1)

    print(f"  Found {len(df)} responses")
    print()

    # Verify required columns exist
    required_cols = [config.EXCEL_COL_CODE, config.EXCEL_COL_NAME, config.EXCEL_COL_WRITING]
    missing_cols = [col for col in required_cols if col not in df.columns]

    if missing_cols:
        print("ERROR: Excel file is missing required columns!")
        print(f"\nExpected columns (check config.py):")
        for col in required_cols:
            status = "✓" if col in df.columns else "✗"
            print(f"  {status} {col}")
        print(f"\nActual columns in Excel file:")
        for col in df.columns:
            print(f"  - {col}")
        print("\nPlease update config.py EXCEL_COL_* constants to match your Forms export.")
        sys.exit(1)

    # Process each response
    print("Processing responses and generating new URLs...")
    print()

    updated_count = 0
    unmatched_responses = []

    for idx, row in df.iterrows():
        response_code = str(row[config.EXCEL_COL_CODE]).strip().upper()
        response_name = str(row[config.EXCEL_COL_NAME]).strip()
        writing_text = str(row[config.EXCEL_COL_WRITING]).strip()

        # Match by student code (much more reliable than name matching)
        if response_code not in students:
            unmatched_responses.append(f"{response_code} ({response_name})")
            print(f"  ⚠ WARNING: Code '{response_code}' not found in students.csv")
            continue

        student_code = response_code

        # Calculate word count
        word_count = len(writing_text.split())

        # Generate progress message
        progress_message = generate_progress_message(word_count)

        # Generate new prefilled URL for Session 2
        new_url = generate_prefilled_url(
            student_code=student_code,
            student_name=response_name,
            include_writing=True,
            writing_text=writing_text,
            writing_info=progress_message
        )

        # Update student record
        students[student_code]['url'] = new_url
        students[student_code]['has_response'] = True
        students[student_code]['word_count'] = word_count

        # Display status
        print(f"  {student_code}: {response_name}")
        print(f"    Words: {word_count}")

        # Show word count feedback
        if word_count < config.WORD_COUNT_MIN:
            print(f"    Status: Needs more words")
        elif word_count > config.WORD_COUNT_MAX:
            print(f"    Status: Consider shortening")
        else:
            print(f"    Status: Good length")

        print(f"    URL: {len(new_url)} characters")
        print()

        updated_count += 1

    # Check for students without responses
    students_without_response = []
    for code, student in students.items():
        if not student.get('has_response', False):
            students_without_response.append(f"{code} ({student['name']})")

    # Write updated students.csv
    print(f"Writing updated URLs to students.csv...")
    fieldnames = ['code', 'name', 'url']

    with open('students.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for code, student in students.items():
            writer.writerow({
                'code': code,
                'name': student['name'],
                'url': student.get('url', '')
            })

    print()
    print("="*60)
    print("Summary")
    print("="*60)
    print(f"✓ Successfully regenerated URLs for {updated_count} students")

    if students_without_response:
        print(f"\n⚠ {len(students_without_response)} students have NOT submitted yet:")
        for student in students_without_response:
            print(f"  - {student}")

    if unmatched_responses:
        print(f"\n⚠ {len(unmatched_responses)} responses could not be matched:")
        for entry in unmatched_responses:
            print(f"  - {entry}")

    print()
    print("Next steps:")
    print("  1. Restart Flask server (Ctrl+C then: python app.py)")
    print("     OR visit: http://YOUR_IP:5000/reload")
    print("  2. Students enter their codes for Session 2")
    print("  3. They will see:")
    print("     - Their writing from Session 1")
    print("     - Word count and feedback")
    print()


def main():
    """Main entry point."""

    if len(sys.argv) < 2:
        print("Usage: python regenerate_links.py <responses.xlsx>")
        print("\nExample:")
        print("  python regenerate_links.py responses.xlsx")
        print("\nDownload responses.xlsx from Microsoft Forms:")
        print("  1. Open your Form")
        print("  2. Go to 'Responses' tab")
        print("  3. Click 'Open in Excel' or export to Excel")
        print("  4. Save as responses.xlsx")
        sys.exit(1)

    excel_file = sys.argv[1]
    regenerate_links(excel_file)


if __name__ == "__main__":
    main()
