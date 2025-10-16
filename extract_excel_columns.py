#!/usr/bin/env python3
"""
Extract Excel column names from Microsoft Forms export and update config.py

This utility helps you configure the Excel column mappings by automatically
extracting column names from an exported Forms response file.

Usage:
    python extract_excel_columns.py responses.xlsx

The script will:
1. Read the Excel file from Microsoft Forms
2. Show you all column names
3. Try to identify which columns match which config variables
4. Ask for confirmation before updating config.py
"""

import sys
import pandas as pd
from pathlib import Path


def extract_columns_from_excel(excel_path):
    """
    Extract column names from Excel export.

    Args:
        excel_path: Path to the Excel file

    Returns:
        list of column names
    """
    try:
        df = pd.read_excel(excel_path)
        return list(df.columns)
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        sys.exit(1)


def identify_column_mappings(columns):
    """
    Try to identify which columns match which config variables.

    Args:
        columns: List of column names from Excel

    Returns:
        dict mapping config variable names to column names
    """
    identified = {}

    # Common patterns for different fields (order matters - more specific first)
    patterns = {
        'EXCEL_COL_TIMESTAMP': ['start time', 'timestamp', 'completion time'],
        'EXCEL_COL_CODE': ['student code', 'student id'],
        'EXCEL_COL_NAME': ['name', 'student name', 'full name'],
        'EXCEL_COL_WRITING': ['writing', 'newsletter', 'content', 'text', 'your writing'],
    }

    for col in columns:
        col_lower = col.lower()

        for config_name, keywords in patterns.items():
            # Check for exact or partial matches
            for keyword in keywords:
                if keyword == col_lower or keyword in col_lower:
                    # If not already identified, or if this is a better match
                    if config_name not in identified:
                        identified[config_name] = col
                        break
                    # Handle edge case: if we found "Name1" and already have "Name", prefer the one with number
                    elif config_name == 'EXCEL_COL_NAME':
                        # Prefer columns with numbers (e.g., "Name1" over "Name")
                        if any(c.isdigit() for c in col) and not any(c.isdigit() for c in identified[config_name]):
                            identified[config_name] = col
                            break
                    # For code field, prefer "Student Code" over just "Id"
                    elif config_name == 'EXCEL_COL_CODE':
                        if 'student' in col_lower and 'student' not in identified[config_name].lower():
                            identified[config_name] = col
                            break

    return identified


def update_config(column_mapping):
    """
    Update config.py with the extracted column names.

    Args:
        column_mapping: Dict of config variable names to column names
    """
    with open('config.py', 'r') as f:
        lines = f.readlines()

    updated_lines = []
    for line in lines:
        updated = False

        for config_var, col_name in column_mapping.items():
            if line.startswith(f'{config_var} = '):
                # Preserve any inline comments
                comment = ''
                if '#' in line:
                    comment = '  ' + line.split('#', 1)[1].rstrip()
                updated_lines.append(f'{config_var} = "{col_name}"{comment}\n')
                updated = True
                break

        if not updated:
            updated_lines.append(line)

    with open('config.py', 'w') as f:
        f.writelines(updated_lines)


def main():
    """Main script flow."""

    print("=" * 70)
    print("Microsoft Forms Excel Column Extractor")
    print("=" * 70)
    print()
    print("This tool will extract column names from your Forms export")
    print("and automatically update config.py")
    print()
    print("=" * 70)
    print()

    # Check if Excel file path provided
    if len(sys.argv) < 2:
        print("Usage: python extract_excel_columns.py <excel_file.xlsx>")
        print()
        print("Example:")
        print("  python extract_excel_columns.py responses.xlsx")
        sys.exit(1)

    excel_path = sys.argv[1]

    # Verify file exists
    if not Path(excel_path).exists():
        print(f"Error: File not found: {excel_path}")
        sys.exit(1)

    print(f"Reading Excel file: {excel_path}")
    print()

    # Extract columns
    columns = extract_columns_from_excel(excel_path)

    print("Found columns:")
    print()
    for i, col in enumerate(columns, 1):
        print(f"  {i}. {col}")
    print()

    # Try to identify columns
    identified = identify_column_mappings(columns)

    print("=" * 70)
    print("Column identification:")
    print("=" * 70)
    print()

    expected_mappings = {
        'EXCEL_COL_TIMESTAMP': 'Timestamp',
        'EXCEL_COL_CODE': 'Student Code',
        'EXCEL_COL_NAME': 'Student Name',
        'EXCEL_COL_WRITING': 'Newsletter Content',
    }

    if len(identified) == len(expected_mappings):
        print(f"✓ Successfully identified all {len(expected_mappings)} columns!")
    else:
        print(f"⚠ Only identified {len(identified)}/{len(expected_mappings)} columns")
        print("  You may need to manually verify config.py after update")

    print()

    # Show identified mappings
    for config_var in expected_mappings.keys():
        if config_var in identified:
            print(f"  {config_var}")
            print(f"    → \"{identified[config_var]}\"")
            print()
        else:
            print(f"  {config_var}")
            print(f"    ⚠ Not identified")
            print()

    # Show missing mappings
    missing = set(expected_mappings.keys()) - set(identified.keys())

    if missing:
        print("⚠ Could not auto-identify these config variables:")
        for var in missing:
            print(f"  - {var}")
        print()
        print("  You'll need to manually match them in config.py")
        print("  Available columns:")
        for col in columns:
            if col not in identified.values():
                print(f"    - \"{col}\"")
        print()

    # Confirm update
    print("=" * 70)
    response = input("\nUpdate config.py with these values? (yes/no): ").strip().lower()

    if response not in ['yes', 'y']:
        print("\nCancelled. No changes made.")
        sys.exit(0)

    # Update config
    update_config(identified)

    print("\n" + "=" * 70)
    print("✓ config.py updated successfully!")
    print("=" * 70)
    print()

    if missing:
        print("⚠ IMPORTANT: Some columns could not be auto-identified")
        print("  Please open config.py and manually verify/update:")
        for var in missing:
            print(f"    - {var}")
        print()

    print("Next steps:")
    print("  1. Review config.py to ensure all column names are correct")
    print("  2. Run: python regenerate_links.py " + excel_path)
    print()


if __name__ == "__main__":
    main()
