#!/bin/sh

set -e

# Django 관련 초기화 작업
python manage.py collectstatic --noinput
python manage.py migrate

# Gunicorn을 사용하여 Django 애플리케이션 실행
exec gunicorn mustgou.wsgi:application --bind 0.0.0.0:8000
