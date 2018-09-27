#!/bin/sh

python /code/manage.py makemigrations --noinput
python manage.py migrate                  # Apply database migrations
python manage.py collectstatic --noinput  # Collect static files

# Start Gunicorn
exec gunicorn lws.wsgi:application \
  --bind 0.0.0.0:8000