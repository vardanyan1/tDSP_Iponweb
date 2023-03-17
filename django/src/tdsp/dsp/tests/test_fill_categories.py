from django.test import TestCase
from ..models.categories_model import CategoryModel


class TestCategoryModel(TestCase):

    def test_create_category(self):
        category = CategoryModel.objects.create(
            code='G01',
            name='Games',
            parent=None
        )
        self.assertEqual(category.code, 'G01')
        self.assertEqual(category.name, 'Games')
        self.assertIsNone(category.parent)

    def test_create_subcategory(self):
        parent_category = CategoryModel.objects.create(
            code='G01',
            name='Games',
            parent=None
        )
        subcategory = CategoryModel.objects.create(
            code='G01.1',
            name='Action Games',
            parent=parent_category
        )
        self.assertEqual(subcategory.code, 'G01.1')
        self.assertEqual(subcategory.name, 'Action Games')
        self.assertEqual(subcategory.parent, parent_category)
