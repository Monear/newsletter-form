#!/usr/bin/env python3
"""Create students.xlsx.template as a proper Excel file"""
import pandas as pd

data = {
    'code': ['STU001', 'STU002', 'STU003'],
    'name': ['Example Student 1', 'Example Student 2', 'Example Student 3'],
    'url': ['', '', '']
}

df = pd.DataFrame(data)
df.to_excel('students.xlsx.template', index=False)
print("✓ Created students.xlsx.template as Excel file")
