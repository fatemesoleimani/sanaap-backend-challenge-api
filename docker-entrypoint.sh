#!/bin/sh
set -e

# Run migrations
poetry run python manage.py migrate

# Create superuser if not exists
echo "from django.contrib.auth import get_user_model; User = get_user_model(); \
if not User.objects.filter(username='admin').exists(): \
    User.objects.create_superuser(username='admin', email='admin@example.com', password='admin123', role='admin')" \
| poetry run python manage.py shell

# Start Django server
exec poetry run python manage.py runserver 0.0.0.0:8000
