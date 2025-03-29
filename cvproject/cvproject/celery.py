import os
from celery import Celery

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE', 'cvproject.settings')

app = Celery('cvproject')

# Load settings from Django settings file using CELERY_ prefix
app.config_from_object('django.conf:settings', namespace='CELERY')

# Autodiscover tasks in installed apps
app.autodiscover_tasks()
