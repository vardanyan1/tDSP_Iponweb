import pandas as pd
from django.core.management.base import BaseCommand
from ...models.categories_model import CategoryModel, SubcategoryModel


class Command(BaseCommand):
    help = 'Imports categories and subcategories from an xlsx file'

    # TODO: add logic to check if already migrated skip this part

    def add_arguments(self, parser):
        parser.add_argument('file_path', help='Path to the xlsx file')

    def handle(self, *args, **options):
        file_path = options['file_path']
        categories_df = pd.read_excel(file_path, sheet_name="Sheet1", engine='openpyxl', usecols=['IAB Code', 'tier', 'IAB Category'])
        categories_df.dropna(inplace=True)

        for _, row in categories_df.iterrows():
            code, tier, category = row.values
            if '-' not in code:
                category, _ = CategoryModel.objects.get_or_create(code=code,
                                                                  tier=tier, category=category)

            if '-' in code:
                parent_code, _ = code.split('-')
                parent_category = CategoryModel.objects.get(code=parent_code)

                subcategory, _ = SubcategoryModel.objects.get_or_create(
                    code=code, tier=tier, subcategory=category, category=parent_category)

        self.stdout.write(self.style.SUCCESS('Successfully imported categories and subcategories'))

