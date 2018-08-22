#!/usr/bin/env bash
echo "Waiting for postgres..."

while ! nc -z looker-db 5432; do
    sleep 0.1
done

echo "PostgresSQL started"

python manage.py run -h 0.0.0.0