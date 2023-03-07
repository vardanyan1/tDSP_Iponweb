import pandas as pd
from django.core.management.base import BaseCommand
from ...models.categories_model import CategoryModel, SubcategoryModel


class Command(BaseCommand):
    help = 'Imports categories and subcategories from an xlsx file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', help='Path to the xlsx file')

    def handle(self, *args, **options):
        file_path = options['file_path']
        categories_df = pd.read_excel(file_path, sheet_name="Sheet1", engine='openpyxl', usecols=['IAB Code', 'Tier', 'IAB Category'])
        categories_df.dropna(inplace=True)

        for _, row in categories_df.iterrows():
            iab_code, tier, iab_category = row.values
            if '-' not in iab_code:
                category, _ = CategoryModel.objects.get_or_create(IAB_Code=iab_code,
                                                                  Tier=tier, IAB_Category=iab_category)

            if '-' in iab_code:
                parent_iab_code, _ = iab_code.split('-')
                parent_category = CategoryModel.objects.get(IAB_Code=parent_iab_code)

                subcategory, _ = SubcategoryModel.objects.get_or_create(
                    IAB_Code=iab_code, Tier=tier, IAB_Subcategory=iab_category, category=parent_category)

        self.stdout.write(self.style.SUCCESS('Successfully imported categories and subcategories'))

