from django.db import models


class CategoryModel(models.Model):
    IAB_Code = models.CharField(max_length=10)
    Tier = models.CharField(max_length=10)
    IAB_Category = models.CharField(max_length=100)

    def __str__(self):
        return self.IAB_Category


class SubcategoryModel(models.Model):
    IAB_Code = models.CharField(max_length=10)
    Tier = models.CharField(max_length=10)
    IAB_Subcategory = models.CharField(max_length=100)
    category = models.ForeignKey(CategoryModel, on_delete=models.CASCADE)

    def __str__(self):
        return self.IAB_Subcategory
