web: gunicorn django-vladly.wsgi:application --log-level debug
worker: celery -A django-vladly worker --beat --concurrency 10 -l info
# beat: celery -A django-vladly beat

web: gunicorn django-vladly.wsgi:application --log-file -
worker: celery -A django-vladly worker -l info -B
