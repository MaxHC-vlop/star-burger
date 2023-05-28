#!/bin/sh

echo "Start makemigrations..."
python manage.py makemigrations --dry-run --check &&
echo "Start migrate..."
python manage.py migrate --noinput &&
echo "Start collectstatic..."
python manage.py collectstatic --noinput &&
echo "Start production server..."
gunicorn -b 0.0.0.0:8080 star_burger.wsgi:application