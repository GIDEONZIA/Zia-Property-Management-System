#!/bin/bash

# Navigate to your Django project directory
cd /path/to/your/project  # <-- Change this to your actual project path

# Activate virtual environment (optional but recommended)
source /path/to/venv/bin/activate  # <-- Change this if you use a virtualenv

# Run Django shell command to delete all LogEntry records
python manage.py shell <<EOF
from django.contrib.admin.models import LogEntry
LogEntry.objects.all().delete()
print("✅ Admin log entries cleared.")
EOF

