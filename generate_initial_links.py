#!/usr/bin/env python3
"""
Generate initial prefilled Microsoft Forms URLs for students.

This script reads student information from students.csv and generates
prefilled Form URLs for Session 1 (with name and prompt only).

Usage:
    python generate_initial_links.py
"""

import csv
from urllib.parse import urlencode, quote
import sys
import config

def generate_prefilled_url(student_code, student_name, include_writing=False, writing_text="", writing_info=""):
    """
    Generate a prefilled Microsoft Forms URL.

    Args:
        student_code: Student code (e.g., STU001)
        student_name: Name of the student
        include_writing: Whether to include previous writing (Session 2)
        writing_text: Previous writing text (for Session 2)
        writing_info: Instructions (Session 1) or progress message (Session 2)

    Returns:
        Complete prefilled URL
    """
    params = {
        config.FIELD_STUDENT_CODE: student_code,
        config.FIELD_STUDENT_NAME: student_name,
    }

    # For Session 2, include previous writing
    if include_writing and writing_text:
        params[config.FIELD_WRITING] = writing_text

    # Include writing info (instructions in Session 1, progress in Session 2)
    if writing_info:
        params[config.FIELD_WRITING_INFO] = writing_info

    # Generate URL with encoded parameters
    # Base URL already has ?id=..., so we use & for our parameters
    # Use quote_via=quote to encode spaces as %20 instead of +
    url = config.BASE_FORM_URL + "&" + urlencode(params, quote_via=quote)

    return url


def validate_config():
    """Validate that config.py has been properly set up."""
    errors = []

    if config.BASE_FORM_URL == "YOUR_FORM_URL_HERE":
        errors.append("BASE_FORM_URL not configured in config.py")

    if config.FIELD_STUDENT_CODE == "entry.YOUR_CODE_FIELD_ID":
        errors.append("FIELD_STUDENT_CODE not configured in config.py")

    if config.FIELD_STUDENT_NAME == "entry.YOUR_NAME_FIELD_ID":
        errors.append("FIELD_STUDENT_NAME not configured in config.py")

    if config.FIELD_WRITING == "entry.YOUR_WRITING_FIELD_ID":
        errors.append("FIELD_WRITING not configured in config.py")

    if config.FIELD_WRITING_INFO == "entry.YOUR_WRITING_INFO_FIELD_ID":
        errors.append("FIELD_WRITING_INFO not configured in config.py")

    if errors:
        print("ERROR: Configuration incomplete!")
        print("\nPlease update config.py with your Microsoft Forms field IDs:")
        for error in errors:
            print(f"  - {error}")
        print("\nSee README.md for setup instructions.")
        return False

    return True


def main():
    """Generate initial prefilled URLs for all students."""

    # Validate configuration
    if not validate_config():
        sys.exit(1)

    # Check if students.csv exists
    try:
        with open('students.csv', 'r') as f:
            reader = csv.DictReader(f)
            students = list(reader)
    except FileNotFoundError:
        print("ERROR: students.csv not found!")
        print("\nPlease create students.csv with columns: code,name")
        print("Example:")
        print("  code,name")
        print("  STU001,John Doe")
        print("  STU002,Jane Smith")
        sys.exit(1)

    # Validate CSV structure
    if not students:
        print("ERROR: students.csv is empty!")
        sys.exit(1)

    required_columns = ['code', 'name']
    if not all(col in students[0] for col in required_columns):
        print(f"ERROR: students.csv must have columns: {', '.join(required_columns)}")
        print(f"Found columns: {', '.join(students[0].keys())}")
        sys.exit(1)

    # Generate URLs for each student
    print(f"Generating prefilled URLs for {len(students)} students...")
    print()

    updated_students = []
    for student in students:
        code = student['code'].strip()
        name = student['name'].strip()

        # Generate initial URL (Session 1)
        url = generate_prefilled_url(
            student_code=code,
            student_name=name,
            writing_info=config.WRITING_INFO_SESSION_1
        )

        # Add URL to student record
        student['url'] = url
        updated_students.append(student)

        print(f"  {code}: {name}")
        print(f"    → {url[:80]}..." if len(url) > 80 else f"    → {url}")
        print()

    # Write updated CSV with URLs
    fieldnames = ['code', 'name', 'url']
    with open('students.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(updated_students)

    print(f"✓ Successfully generated {len(updated_students)} prefilled URLs")
    print(f"✓ Updated students.csv with URLs")
    print()
    print("Next steps:")
    print("  1. Start the Flask server: python app.py")
    print("  2. Students can access via: http://YOUR_IP:5000")
    print("  3. After Session 1, download responses and run: python regenerate_links.py responses.xlsx")


if __name__ == "__main__":
    main()
