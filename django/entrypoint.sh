#!/bin/sh

echo "Waiting for postgres..."

while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  sleep 0.1
done

echo "PostgreSQL started"

python src/manage.py migrate

if [ ! -f categories/initiated.txt ]; then
    python src/manage.py import_categories categories/Content-Taxonomy-1.0.xlsx
    touch categories/initiated.txt
fi;

exec "$@"