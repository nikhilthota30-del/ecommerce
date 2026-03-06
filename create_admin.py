import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project_name.settings') # Replace 'your_project_name' with your actual folder name
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()
username = 'nikhiladmin'
email = 'admin@example.com'
password = 'password123'

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print(f"Superuser {username} created successfully!")
else:
    print(f"Superuser {username} already exists.")