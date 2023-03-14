import openpyxl
from django.core.management.base import BaseCommand
from ...models.categories_model import CategoryModel, SubcategoryModel


class Command(BaseCommand):
    help = 'Imports categories and subcategories from an xlsx file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', help='Path to the xlsx file')

    def handle(self, *args, **options):
        file_path = options['file_path']
        workbook = openpyxl.load_workbook(filename=file_path, read_only=True, data_only=True)
        worksheet = workbook['Sheet1']

        categories = []
        for row in worksheet.iter_rows(min_row=2, values_only=True):
            code, _, category, *_ = row
            if code is not None and category is not None:
                categories.append({'code': code, 'category': category})

        for category in categories:
            code = category['code']
            category_name = category['category']

            if '-' not in code:
                category, _ = CategoryModel.objects.get_or_create(code=code, category=category_name)

            elif '-' in code:
                parent_code, _ = code.split('-')
                parent_category = CategoryModel.objects.get(code=parent_code)

                subcategory, _ = SubcategoryModel.objects.get_or_create(
                    code=code, subcategory=category_name, category=parent_category)

        self.stdout.write(self.style.SUCCESS('Successfully imported categories and subcategories'))

