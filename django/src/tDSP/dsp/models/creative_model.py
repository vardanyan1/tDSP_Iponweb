from django.db import models
from ..models.categories_model import SubcategoryModel
from ..models.campaign_model import CampaignModel


class CreativeModel(models.Model):

    external_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    url = models.URLField(max_length=500)
    categories = models.ManyToManyField(SubcategoryModel)
    campaign = models.ForeignKey(CampaignModel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.external_id})"