#!/bin/sh

echo "Apply database migrations"
python sw_backend/manage.py migrate

echo "Starting server"
python sw_backend/manage.py runserver 0.0.0.0:8000
