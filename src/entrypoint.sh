#!/bin/sh
export $(cat .env | grep NEW_RELIC_LICENSE_KEY)

# Run migrations
python manage.py migrate

# Start app
NEW_RELIC_CONFIG_FILE=newrelic.ini newrelic-admin run-program gunicorn --bind 0.0.0.0:8000 main.wsgi:application