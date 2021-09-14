#!/bin/bash
python manage.py migrate && \
python manage.py collectstatic --no-input && \
gunicorn api_foodgram.wsgi:application --bind 0.0.0.0:8000