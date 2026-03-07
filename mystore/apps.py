from django.apps import AppConfig
from django.db.models.signals import post_migrate

class MystoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mystore'

    def ready(self):
        post_migrate.connect(create_superuser, sender=self)

def create_superuser(sender, **kwargs):
    from django.contrib.auth import get_user_model
    User = get_user_model()
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'YourPassword123')