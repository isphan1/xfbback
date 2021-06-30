release: python3 manage.py migrate
web: gunicorn box.wsgi:application --log-file - --log-level debug
