"""
config.template.py - Configuration Template
===========================================
Copy this file to config.py and fill in your actual values.

INSTRUCTIONS:
1. Copy this file: copy config.template.py config.py
2. Edit config.py with your real credentials
3. Never commit config.py to GitHub!

This template is safe to commit to version control.
"""

# Database Configuration Template
DATABASE_CONFIG = {
    'host': 'YOUR_DATABASE_SERVER',     # e.g., 'localhost' or 'C-GOA-APM-13251'
    'port': '5432',                     # PostgreSQL default port
    'database': 'YOUR_DATABASE_NAME',   # e.g., 'Main'
    'user': 'YOUR_DB_USERNAME',         # e.g., 'postgres'
    'password': 'YOUR_DB_PASSWORD',     # Your actual database password
    'schema': 'YOUR_SCHEMA_NAME'        # e.g., 'wrmm_sopan'
}

# Output Settings
OUTPUT_SETTINGS = {
    'enable_database': True,   # Push data to database
    'enable_files': False      # Create CSV/Excel files (set to True if you want both)
}

# Optional: Other configuration settings
PROCESSING_SETTINGS = {
    'start_week': 33,
    'end_week': 38,
    'current_year': 2025
}