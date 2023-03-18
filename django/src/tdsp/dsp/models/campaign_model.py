from django.db import models

from ..models.game_config_model import ConfigModel


class CampaignModel(models.Model):

    name = models.CharField(max_length=30)
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    config = models.ForeignKey(ConfigModel, on_delete=models.CASCADE, limit_choices_to={'current': True})
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
