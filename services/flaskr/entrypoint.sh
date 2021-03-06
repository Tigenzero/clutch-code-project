#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 1.0
    done

    echo "Exiting PostgreSQL wait"
fi

echo "PostgreSQL started"

python3 manage.py create_db

python3 manage.py seed_db

exec "$@"