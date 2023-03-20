from django.db import models


class CategoryModel(models.Model):
    """
    Represents a category in the system.

    Attributes:
        code (str): The unique code for the category.
        name (str): The name of the category.
        parent (CategoryModel, optional): The parent category for the current category.

    Methods:
        __str__(): Returns a string representation of the CategoryModel instance.
    """

    code = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    parent = models.ForeignKey("self", null=True, on_delete=models.CASCADE)

    def __str__(self) -> str:
        """
        Returns a string representation of the CategoryModel instance.

        Returns:
            str: A string representing the CategoryModel instance.
        """
        return f"{self.name}"
