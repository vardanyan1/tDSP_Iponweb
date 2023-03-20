from django.db import models
from ..models.categories_model import CategoryModel
from ..models.campaign_model import CampaignModel


class CreativeModel(models.Model):
    """
    Represents a creative in the system.

    Attributes:
        external_id (str): The unique external ID for the creative.
        name (str): The name of the creative.
        url (str): The URL of the creative.
        categories (List[CategoryModel]): The categories associated with the creative.
        campaign (CampaignModel): The campaign associated with the creative.
        created_at (datetime): The datetime the creative was created.
        updated_at (datetime): The datetime the creative was last updated.

    Methods:
        __str__(): Returns a string representation of the CreativeModel instance.
    """
    external_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    url = models.URLField(max_length=500)
    categories = models.ManyToManyField(CategoryModel)
    campaign = models.ForeignKey(CampaignModel, on_delete=models.CASCADE, limit_choices_to={'config__current': True})
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
       Returns a string representation of the CreativeModel instance.

       Returns:
           str: A string representing the CreativeModel instance.
       """
        return f"{self.name}, ext_id: {self.external_id}"
