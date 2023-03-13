#!/bin/sh

echo "Waiting for postgres..."

while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  sleep 0.1
done

echo "PostgreSQL started"

#  TODO:Write better code cuz if theres no migrations folder this wont work
# Check if migrations have been applied for the dsp app
#if python src/manage.py showmigrations | grep -q "(no migrations)"; then
if [ ! -d "src/tdsp/dsp/migrations" ]; then
    echo "Migrations for dsp app not applied. Running makemigrations and migrate..."
    python src/manage.py makemigrations dsp
    python src/manage.py migrate
    python src/manage.py import_categories categories/Content-Taxonomy-1.0.xlsx
    echo "Creating superuser..."
    python src/manage.py createsuperuser --email=admin@admin.com --noinput
    echo "Superuser created!"
else
    ls
    echo "Migrations for dsp app already applied. Skipping makemigrations and migrate."
fi

exec "$@"