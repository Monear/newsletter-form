#!/usr/bin/env python3
"""
Flask redirect server for student writing assignment.

Students enter their code and are redirected to their personalized
Microsoft Forms URL.

Usage:
    python app.py
"""

from flask import Flask, render_template_string, request, redirect
import pandas as pd
import sys
from pathlib import Path

# Add parent directory to path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent))
import config

app = Flask(__name__)

# In-memory cache of student mappings
STUDENT_MAPPINGS = {}


def load_student_mappings():
    """Load student code → URL mappings from students.xlsx."""
    global STUDENT_MAPPINGS
    STUDENT_MAPPINGS = {}

    # Path to students.xlsx in parent directory
    students_file = Path(__file__).parent.parent / 'students.xlsx'

    try:
        df = pd.read_excel(students_file)

        for _, row in df.iterrows():
            code = str(row['code']).strip().upper()
            url = str(row.get('url', '')).strip()

            if url and url != 'nan':
                STUDENT_MAPPINGS[code] = {
                    'name': str(row['name']).strip(),
                    'url': url
                }

        print(f"Loaded {len(STUDENT_MAPPINGS)} student mappings")
        return True

    except FileNotFoundError:
        print("ERROR: students.xlsx not found!")
        print("Run: python src/generate_initial_links.py")
        return False
    except Exception as e:
        print(f"ERROR loading students.xlsx: {e}")
        return False


# HTML template for the entry page
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Student Writing Portal</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }

        .container {
            background: white;
            padding: 40px;
            border-radius: 12px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            max-width: 450px;
            width: 100%;
        }

        h1 {
            color: #333;
            margin-bottom: 10px;
            font-size: 28px;
            text-align: center;
        }

        .subtitle {
            color: #666;
            text-align: center;
            margin-bottom: 30px;
            font-size: 14px;
        }

        .form-group {
            margin-bottom: 20px;
        }

        label {
            display: block;
            margin-bottom: 8px;
            color: #333;
            font-weight: 500;
        }

        input[type="text"] {
            width: 100%;
            padding: 12px 16px;
            font-size: 16px;
            border: 2px solid #e0e0e0;
            border-radius: 6px;
            transition: border-color 0.3s;
            text-transform: uppercase;
        }

        input[type="text"]:focus {
            outline: none;
            border-color: #667eea;
        }

        button {
            width: 100%;
            padding: 14px;
            font-size: 16px;
            font-weight: 600;
            color: white;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border: none;
            border-radius: 6px;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
        }

        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
        }

        button:active {
            transform: translateY(0);
        }

        .error {
            background: #fee;
            color: #c33;
            padding: 12px;
            border-radius: 6px;
            margin-bottom: 20px;
            border-left: 4px solid #c33;
            font-size: 14px;
        }

        .info {
            background: #f0f9ff;
            color: #0369a1;
            padding: 12px;
            border-radius: 6px;
            margin-top: 20px;
            border-left: 4px solid #0369a1;
            font-size: 13px;
        }

        .stats {
            text-align: center;
            color: #999;
            font-size: 12px;
            margin-top: 20px;
            padding-top: 20px;
            border-top: 1px solid #eee;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Writing Assignment</h1>
        <p class="subtitle">Enter your student code to begin</p>

        {% if error %}
        <div class="error">
            {{ error }}
        </div>
        {% endif %}

        <form method="POST">
            <div class="form-group">
                <label for="code">Student Code</label>
                <input
                    type="text"
                    id="code"
                    name="code"
                    placeholder="e.g., STU001"
                    autofocus
                    required
                    autocomplete="off"
                >
            </div>
            <button type="submit">Start Writing →</button>
        </form>

        <div class="info">
            <strong>Instructions:</strong>
            <ul style="margin-left: 20px; margin-top: 8px;">
                <li>Enter your assigned code above</li>
                <li>Complete your writing assignment (~250 words)</li>
                <li>Upload your picture</li>
                <li>Click Submit when finished</li>
            </ul>
        </div>

        <div class="stats">
            {{ student_count }} students registered
        </div>
    </div>
</body>
</html>
"""


@app.route('/', methods=['GET', 'POST'])
def index():
    """Main entry page - student enters code."""

    if request.method == 'POST':
        code = request.form.get('code', '').strip().upper()

        if not code:
            return render_template_string(
                HTML_TEMPLATE,
                error="Please enter your student code.",
                student_count=len(STUDENT_MAPPINGS)
            )

        # Check if code exists
        if code in STUDENT_MAPPINGS:
            url = STUDENT_MAPPINGS[code]['url']
            return redirect(url)
        else:
            return render_template_string(
                HTML_TEMPLATE,
                error=f"Code '{code}' not found. Please check your code and try again.",
                student_count=len(STUDENT_MAPPINGS)
            )

    # GET request - show entry form
    return render_template_string(
        HTML_TEMPLATE,
        student_count=len(STUDENT_MAPPINGS)
    )


@app.route('/reload')
def reload_mappings():
    """Reload student mappings from CSV (useful for updates between sessions)."""
    if load_student_mappings():
        return f"<h1>Reloaded {len(STUDENT_MAPPINGS)} student mappings</h1><a href='/'>Back to entry page</a>"
    else:
        return "<h1>Error reloading mappings</h1><p>Check console for details</p>", 500


@app.route('/admin')
def admin():
    """Simple admin page showing all student codes and names."""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Admin - Student List</title>
        <style>
            body { font-family: sans-serif; max-width: 800px; margin: 40px auto; padding: 20px; }
            table { width: 100%; border-collapse: collapse; margin-top: 20px; }
            th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
            th { background: #667eea; color: white; }
            tr:hover { background: #f5f5f5; }
            .header { display: flex; justify-content: space-between; align-items: center; }
            .button {
                padding: 8px 16px;
                background: #667eea;
                color: white;
                text-decoration: none;
                border-radius: 4px;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>Student List</h1>
            <a href="/" class="button">Back to Entry</a>
        </div>
        <p><strong>{{ count }}</strong> students registered</p>
        <table>
            <tr>
                <th>Code</th>
                <th>Name</th>
                <th>Status</th>
            </tr>
            {% for code, data in students.items() %}
            <tr>
                <td><strong>{{ code }}</strong></td>
                <td>{{ data.name }}</td>
                <td>✓ URL ready</td>
            </tr>
            {% endfor %}
        </table>
    </body>
    </html>
    """
    return render_template_string(
        html,
        students=STUDENT_MAPPINGS,
        count=len(STUDENT_MAPPINGS)
    )


def main():
    """Start the Flask server."""

    # Load student mappings
    if not load_student_mappings():
        print("\nPlease run: python generate_initial_links.py")
        sys.exit(1)

    print("\n" + "="*60)
    print("Student Writing Portal - Server Starting")
    print("="*60)
    print(f"\nStudents registered: {len(STUDENT_MAPPINGS)}")
    print(f"\nServer will start on: http://{config.FLASK_HOST}:{config.FLASK_PORT}")
    print("\nAccess URLs:")
    print(f"  - Student entry: http://YOUR_IP:{config.FLASK_PORT}/")
    print(f"  - Admin panel:   http://YOUR_IP:{config.FLASK_PORT}/admin")
    print(f"  - Reload data:   http://YOUR_IP:{config.FLASK_PORT}/reload")
    print("\nPress Ctrl+C to stop the server")
    print("="*60 + "\n")

    # Start Flask server
    app.run(
        host=config.FLASK_HOST,
        port=config.FLASK_PORT,
        debug=config.FLASK_DEBUG
    )


if __name__ == "__main__":
    main()
