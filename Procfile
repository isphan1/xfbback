release: python3 manage.py migrate
web: gunicorn dr.wsgi:application --log-file - --log-level debug
