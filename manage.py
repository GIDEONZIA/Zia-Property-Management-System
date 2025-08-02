#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import django

from django.core.management import execute_from_command_line

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "property_mgmt.settings")
    django.setup()  # Initialize Django before accessing models
    execute_from_command_line(sys.argv)

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# The main entry point is already handled above
