#!/usr/bin/env python3
"""
Extract field IDs from a Microsoft Forms prefilled URL and update config.py

This utility helps you configure the system by automatically extracting
field parameter names from a prefilled Forms URL.

Usage:
    python src/utils/extract_form_fields.py

The script will:
1. Prompt you to paste your prefilled Forms URL
2. Parse the URL to extract the base URL and field IDs
3. Show you what it found
4. Ask for confirmation before updating config.py
"""

import sys
from urllib.parse import urlparse, parse_qs
from pathlib import Path


def extract_fields_from_url(url):
    """
    Extract base URL and field parameters from a prefilled Forms URL.

    Args:
        url: The complete prefilled Forms URL

    Returns:
        dict with 'base_url' and 'fields' (dict of field_id: sample_value)
    """
    # Parse the URL
    parsed = urlparse(url)

    # Base URL is everything before the query string
    base_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"

    # If there's a query string, parse it
    if parsed.query:
        base_url += "?" + parsed.query.split('&')[0]  # Keep the ?id=... part

    # Parse all parameters
    # Split by & and parse each parameter
    params = {}
    if '&' in url:
        # Get everything after the first &
        param_string = url.split('&', 1)[1]

        # Parse each parameter
        for param in param_string.split('&'):
            if '=' in param:
                key, value = param.split('=', 1)
                # URL decode for display
                from urllib.parse import unquote
                params[key] = unquote(value.replace('+', ' '))

    return {
        'base_url': base_url,
        'fields': params
    }


def identify_field_types(fields):
    """
    Try to identify which field is which based on the sample values.

    Returns:
        dict mapping our config names to field IDs
    """
    identified = {}

    for field_id, sample_value in fields.items():
        value_lower = sample_value.lower()

        # Try to identify based on sample content
        if 'stu' in value_lower and len(sample_value) < 20:
            identified['FIELD_STUDENT_CODE'] = field_id
        elif any(name_part in value_lower for name_part in ['test', 'john', 'jane', 'nguyen', 'tran']):
            if len(sample_value) < 50:
                identified['FIELD_STUDENT_NAME'] = field_id
        elif len(sample_value) > 100:
            identified['FIELD_WRITING'] = field_id
        elif 'end' in value_lower and 'class' in value_lower:
            identified['FIELD_WRITING_INFO'] = field_id
        elif 'session' in value_lower or 'word' in value_lower:
            identified['FIELD_WRITING_INFO'] = field_id

    return identified


def update_config(base_url, field_mapping):
    """
    Update config.py with the extracted values.

    Args:
        base_url: The base Forms URL
        field_mapping: Dict of config names to field IDs
    """
    # Path to config.py in src directory
    config_file = Path(__file__).parent.parent / 'config.py'

    with open(config_file, 'r') as f:
        lines = f.readlines()

    updated_lines = []
    for line in lines:
        # Update base URL
        if line.startswith('BASE_FORM_URL = '):
            updated_lines.append(f'BASE_FORM_URL = "{base_url}"\n')
        # Update field IDs
        elif line.startswith('FIELD_STUDENT_CODE = ') and 'FIELD_STUDENT_CODE' in field_mapping:
            updated_lines.append(f'FIELD_STUDENT_CODE = "{field_mapping["FIELD_STUDENT_CODE"]}"\n')
        elif line.startswith('FIELD_STUDENT_NAME = ') and 'FIELD_STUDENT_NAME' in field_mapping:
            updated_lines.append(f'FIELD_STUDENT_NAME = "{field_mapping["FIELD_STUDENT_NAME"]}"\n')
        elif line.startswith('FIELD_WRITING = ') and 'FIELD_WRITING' in field_mapping:
            updated_lines.append(f'FIELD_WRITING = "{field_mapping["FIELD_WRITING"]}"\n')
        elif line.startswith('FIELD_WRITING_INFO = ') and 'FIELD_WRITING_INFO' in field_mapping:
            updated_lines.append(f'FIELD_WRITING_INFO = "{field_mapping["FIELD_WRITING_INFO"]}"  # Shows instructions in Session 1, progress in Session 2\n')
        else:
            updated_lines.append(line)

    with open(config_file, 'w') as f:
        f.writelines(updated_lines)


def main():
    """Main script flow."""

    print("=" * 70)
    print("Microsoft Forms Field Extractor")
    print("=" * 70)
    print()
    print("This tool will extract field IDs from your prefilled Forms URL")
    print("and automatically update config.py")
    print()
    print("Steps:")
    print("  1. Create your Microsoft Form with 4 fields:")
    print("     - Name (short text)")
    print("     - Student Code (short text)")
    print("     - Newsletter Content (long text)")
    print("     - Info: (short text)")
    print()
    print("  2. In Forms, click '...' → 'Get pre-filled URL'")
    print("  3. Fill in sample data for ALL fields:")
    print("     - Name: 'Test Student'")
    print("     - Student Code: 'STU001'")
    print("     - Newsletter Content: 'Sample writing text here'")
    print("     - Info: 'Test info'")
    print("  4. Copy the generated URL and paste it below")
    print()
    print("=" * 70)
    print()

    # Get URL from user
    url = input("Paste your prefilled Forms URL here:\n").strip()

    if not url:
        print("\nError: No URL provided!")
        sys.exit(1)

    if 'forms.office.com' not in url:
        print("\nError: This doesn't look like a Microsoft Forms URL!")
        sys.exit(1)

    print("\n" + "=" * 70)
    print("Extracting fields...")
    print("=" * 70)
    print()

    # Extract fields
    result = extract_fields_from_url(url)

    print(f"Base URL: {result['base_url']}")
    print()
    print("Found fields:")
    print()

    for field_id, sample_value in result['fields'].items():
        # Truncate long values
        display_value = sample_value if len(sample_value) < 50 else sample_value[:47] + "..."
        print(f"  {field_id}")
        print(f"    Sample value: '{display_value}'")
        print()

    # Try to identify fields
    identified = identify_field_types(result['fields'])

    print("=" * 70)
    print("Field identification:")
    print("=" * 70)
    print()

    if len(identified) == 4:
        print("✓ Successfully identified all 4 fields!")
    else:
        print(f"⚠ Only identified {len(identified)}/4 fields")
        print("  You may need to manually verify config.py after update")

    print()
    for config_name, field_id in identified.items():
        sample = result['fields'][field_id]
        display_sample = sample if len(sample) < 40 else sample[:37] + "..."
        print(f"  {config_name.replace('FIELD_', '').replace('_', ' ').title()}")
        print(f"    Field ID: {field_id}")
        print(f"    Sample: '{display_sample}'")
        print()

    # Missing fields
    expected_fields = {'FIELD_STUDENT_CODE', 'FIELD_STUDENT_NAME', 'FIELD_WRITING', 'FIELD_WRITING_INFO'}
    missing = expected_fields - set(identified.keys())

    if missing:
        print("⚠ Could not auto-identify these fields:")
        for field in missing:
            print(f"  - {field.replace('FIELD_', '').replace('_', ' ').title()}")
        print()
        print("  You'll need to manually match them in config.py")
        print("  Available field IDs:")
        for field_id in result['fields'].keys():
            if field_id not in identified.values():
                print(f"    - {field_id}")
        print()

    # Confirm update
    print("=" * 70)
    response = input("\nUpdate config.py with these values? (yes/no): ").strip().lower()

    if response not in ['yes', 'y']:
        print("\nCancelled. No changes made.")
        sys.exit(0)

    # Update config
    update_config(result['base_url'], identified)

    print("\n" + "=" * 70)
    print("✓ config.py updated successfully!")
    print("=" * 70)
    print()

    if missing:
        print("⚠ IMPORTANT: Some fields could not be auto-identified")
        print("  Please open config.py and manually verify/update:")
        for field in missing:
            print(f"    - {field}")
        print()

    print("Next steps:")
    print("  1. Review src/config.py to ensure all fields are correct")
    print("  2. Update EXCEL_COL_* in config.py (use extract_excel_columns.py)")
    print("  3. Run: python src/generate_initial_links.py")
    print("  4. Start the server: python src/app.py")
    print()


if __name__ == "__main__":
    main()
