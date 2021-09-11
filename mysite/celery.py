import os
from celery import Celery # noqa


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

app = Celery('mysite_celery')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
