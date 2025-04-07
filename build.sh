#!/usr/bin/env bash
# exit on error
set -o errexit

# Install Python dependencies
pip install -r requirements-prod.txt

# Collect static files
python manage.py collectstatic --no-input

# Create migrations
python manage.py makemigrations

# Run migrations
python manage.py migrate 