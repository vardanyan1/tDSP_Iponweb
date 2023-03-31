from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = 'Checks if the Categories model exists in the database'

    def handle(self, *args, **options):
        table_name = 'dsp_categorymodel'
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT to_regclass('{table_name}');")
            result = cursor.fetchone()
            if result and result[0]:
                self.stdout.write(self.style.SUCCESS('Categories model exists in the database.'))
            else:
                self.stdout.write(self.style.ERROR('Categories model does not exist in the database.'))
