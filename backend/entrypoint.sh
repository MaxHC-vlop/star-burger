#!/bin/sh

# if [ "$DATABASE" = "postgres" ]
# then
#     echo "Waiting for postgres..."

#     while ! nc -z $SQL_HOST $SQL_PORT; do
#       sleep 0.1
#     done

#     echo "PostgreSQL started"
# fi

echo "Start makemigrations..."
python manage.py makemigrations --dry-run --check &&
echo "Start migrate..."
python manage.py migrate --noinput &&
echo "Start collectstatic..."
python manage.py collectstatic --noinput &&
echo "Start server..."
python manage.py runserver 0.0.0.0:8080