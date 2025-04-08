#!/usr/bin/env bash
# exit on error
set -o errexit

# Install Python dependencies
pip install -r requirements.txt

# Create media directory if it doesn't exist and set permissions
mkdir -p media
chmod 755 media

# Collect static files
python manage.py collectstatic --no-input

# Run migrations
python manage.py migrate 