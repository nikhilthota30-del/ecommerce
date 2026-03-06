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



# Create superuser if it doesn't exist
python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'YourPassword123')
    print("Superuser created!")
else:
    print("Superuser already exists.")
END