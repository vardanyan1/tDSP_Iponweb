from django.db import models

from ..models.game_config_model import ConfigModel


class CampaignModel(models.Model):
    """
    Represents a campaign in the system.

    Attributes:
        name (str): The name of the campaign.
        budget (Decimal): The budget allocated to the campaign.
        config (ConfigModel): The game configuration associated with the campaign.
        is_active (bool): Whether the campaign is currently active.

    Methods:
        __str__(): Returns a string representation of the BidResponseModel instance.
    """

    name = models.CharField(max_length=128)
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    config = models.ForeignKey(ConfigModel, on_delete=models.CASCADE, limit_choices_to={'current': True})
    is_active = models.BooleanField(default=True)
    min_bid = models.DecimalField(max_digits=10, decimal_places=2, default=None, null=True)

    def __str__(self) -> str:
        """
        Returns a string representation of the CampaignModel instance.

        Returns:
            str: A string representing the CampaignModel instance.
        """
        return f"{self.name}"
