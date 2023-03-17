from django.db import models
from ..models.campaign_model import CampaignModel


class UserImpression(models.Model):
    user_id = models.CharField(max_length=255)
    campaign = models.ForeignKey(CampaignModel, on_delete=models.CASCADE) # Add a ForeignKey to the CampaignModel
    impressions = models.IntegerField(default=0)

    class Meta:
        unique_together = ('user_id', 'campaign') # Update the unique constraint
