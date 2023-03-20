from django.test import TestCase
from ..models.categories_model import CategoryModel


class TestCategoryModel(TestCase):
    """
     A test case for testing the CategoryModel.

     Methods:
         test_create_category(): Tests creating a category with no parent and checks that the category
                                    is created with the correct data.
         test_create_subcategory(): Tests creating a subcategory with a parent category and checks that the subcategory
                                        is created with the correct data and has the correct parent category.
     """
    def test_create_category(self):
        """
        Tests creating a category with no parent and checks that the category is created with the correct data.
        """
        category = CategoryModel.objects.create(
            code='G01',
            name='Games',
            parent=None
        )
        self.assertEqual(category.code, 'G01')
        self.assertEqual(category.name, 'Games')
        self.assertIsNone(category.parent)

    def test_create_subcategory(self):
        """
        Tests creating a subcategory with a parent category and checks that the subcategory is created with the correct
        data and has the correct parent category.
        """
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
