web: gunicorn mysite.wsgi:application --log-file -
worker: celery -A mysite worker -l info -B
