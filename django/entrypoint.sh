#!/bin/sh

echo "Waiting for postgres..."

while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  sleep 0.1
done

echo "PostgreSQL started"

# Check if migrations have been applied for the dsp app
if python src/manage.py showmigrations | grep -q "(no migrations)"; then
    echo "Migrations for dsp app not applied. Running makemigrations and migrate..."
    python src/manage.py makemigrations dsp
    python src/manage.py migrate
    python src/manage.py import_categories categories/Content-Taxonomy-1.0.xlsx
else
    echo "Migrations for dsp app already applied. Skipping makemigrations and migrate."
fi

exec "$@"