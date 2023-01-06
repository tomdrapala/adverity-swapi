#!/bin/sh

echo "Apply database migrations"
python sw_backend/manage.py migrate

echo "Install fixtures"
python sw_backend/manage.py loaddata sw_backend/people/fixtures/people.json

echo "Starting server"
python sw_backend/manage.py runserver 0.0.0.0:8000
