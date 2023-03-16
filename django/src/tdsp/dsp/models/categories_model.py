from django.db import models


class CategoryModel(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    parent = models.ForeignKey("self", null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
