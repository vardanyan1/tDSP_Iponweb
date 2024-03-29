import openpyxl
from django.core.management.base import BaseCommand
from ...models.categories_model import CategoryModel


class Command(BaseCommand):
    """
    A management command that imports categories and subcategories from an xlsx file.

    Usage:
        python manage.py import_categories <file_path>

    <file_path> is the path to the xlsx file containing the categories and subcategories.

    """
    help = 'Imports categories and subcategories from an xlsx file'

    def add_arguments(self, parser):
        """
        Define command line arguments for the management command.
        """
        parser.add_argument('file_path', help='Path to the xlsx file')

    def handle(self, *args, **options):
        """
        Handle the management command.
        """
        # Check if categories already exist
        if CategoryModel.objects.count() > 0:
            self.stdout.write(self.style.WARNING('Categories and subcategories already exist. Skipping import.'))
            return

        file_path = options['file_path']
        workbook = openpyxl.load_workbook(filename=file_path, read_only=True, data_only=True)
        worksheet = workbook['Sheet1']

        categories = []
        for row in worksheet.iter_rows(min_row=2, values_only=True):
            code, _, name, *_ = row
            if code is not None and name is not None:
                categories.append({'code': code, 'name': name})

        for category in categories:
            code = category['code']
            name = category['name']

            if '-' not in code:
                category = CategoryModel.objects.create(code=code, name=name)

            elif '-' in code:
                parent_code, _ = code.split('-')
                parent_category = CategoryModel.objects.get(code=parent_code)

                subcategory = CategoryModel.objects.create(
                    code=code, name=name, parent=parent_category)

        self.stdout.write(self.style.SUCCESS('Successfully imported categories and subcategories'))
