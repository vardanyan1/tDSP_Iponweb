#!/bin/sh

echo "Waiting for postgres..."

while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  sleep 0.1
done

echo "PostgreSQL started"

# Check if Categories model exists in the database
if python src/manage.py check_categories_exists | grep -q "Categories model does not exist"; then
    echo "Migrations for dsp app not applied. Running migrate..."
    python src/manage.py migrate
    python src/manage.py import_categories categories/Content-Taxonomy-1.0.xlsx
    echo "Collecting static files..."
    python src/manage.py collectstatic --noinput

    echo "Creating superuser..."
    python src/manage.py createsuperuser --email=admin@admin.com --noinput
    echo "Superuser created!"
else
    echo "Migrations for dsp app already applied. Skipping and migrate."
fi

exec /bin/sh -c "cd src/ && gunicorn --bind 0.0.0.0:8000 tdsp.wsgi"