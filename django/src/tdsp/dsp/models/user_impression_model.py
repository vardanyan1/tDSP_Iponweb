from django.db import models
from ..models.campaign_model import CampaignModel


class UserImpression(models.Model):
    """
    Represents a user impression model in the system.

    Attributes:
        user_id (str): The ID of the user associated with the impression.
        campaign (CampaignModel): The campaign associated with the impression.
        impressions (int): The number of impressions.

    Methods:
        __str__(): Returns a string representation of the ConfigModel instance.

    Meta:
        unique_together (tuple): The unique constraint for the model.

    """
    user_id = models.CharField(max_length=255)
    campaign = models.ForeignKey(CampaignModel, on_delete=models.CASCADE)  # Add a ForeignKey to the CampaignModel
    impressions = models.IntegerField(default=0)

    class Meta:
        """"
        Represents the metadata for the UserImpression model.

        Attributes:
            unique_together (tuple): A tuple indicating that the combination of 'user_id' and 'campaign'
                                     should be unique together.
        """
        unique_together = ('user_id', 'campaign')  # Update the unique constraint

    def __str__(self):
        """
        Returns a string representation of the UserImpression instance.

        Returns:
            str: A string representing the UserImpression instance.
        """
        return f"Impression for user {self.user_id} in campaign {self.campaign}"
