#!/usr/bin/env bash
# exit on error
set -o errexit

# Install Python dependencies
pip install -r requirements.txt

# Create media directory if it doesn't exist and set permissions
mkdir -p media
chmod 755 media

# Create directory for CKEditor uploads
mkdir -p media/uploads/ckeditor
chmod 755 media/uploads/ckeditor

# Collect static files
python manage.py collectstatic --no-input --clear

# Run migrations
python manage.py migrate