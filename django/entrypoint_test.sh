#!/bin/sh

echo "Waiting for postgres..."

while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  sleep 0.1
done

echo "PostgreSQL started"

echo "Migrations for dsp app not applied. Running migrate..."
python src/manage.py migrate
python src/manage.py import_categories categories/Content-Taxonomy-1.0.xlsx
echo "Collecting static files..."
python src/manage.py collectstatic --noinput

echo "Creating superuser..."
python src/manage.py createsuperuser --email=admin@admin.com --noinput
echo "Superuser created!"

# Run tests and generate coverage report
echo "Running tests and generating coverage report..."
coverage run src/manage.py test tdsp.dsp.tests
coverage xml -o /code/src/coverage.xml