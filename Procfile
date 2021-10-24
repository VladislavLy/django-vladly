web: gunicorn django-vladly.wsgi:application --log-file -
worker: celery -A django-vladly worker -l info -B
