from django.db import models


class CategoryModel(models.Model):
    code = models.CharField(max_length=10)
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.category


class SubcategoryModel(models.Model):
    code = models.CharField(max_length=10)
    subcategory = models.CharField(max_length=100)
    category = models.ForeignKey(CategoryModel, on_delete=models.CASCADE)

    def __str__(self):
        return self.subcategory
