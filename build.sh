#!/usr/bin/env bash
# exit on error
set -o errexit

# Upgrade pip and related tools first
python -m pip install --upgrade pip setuptools wheel

# Install your requirements
pip install -r requirements.txt

# Run Django commands
python manage.py collectstatic --no-input
python manage.py migrate