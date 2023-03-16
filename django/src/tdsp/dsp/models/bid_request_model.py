from django.db import models
from ..models.game_config_model import ConfigModel
from ..models.categories_model import CategoryModel


class BidRequestModel(models.Model):
    """
    Represents a bid request in the system.
    """
    bid_id = models.CharField(max_length=255, unique=True)
    banner_width = models.IntegerField()
    banner_height = models.IntegerField()
    click_probability = models.FloatField()
    conversion_probability = models.FloatField()
    site_domain = models.CharField(max_length=255)
    ssp_id = models.CharField(max_length=255)
    user_id = models.CharField(max_length=255)
    blocked_categories = models.ManyToManyField(CategoryModel, blank=True, related_name="blocked_bid_requests")
    config = models.ForeignKey(ConfigModel, null=True, on_delete=models.CASCADE, limit_choices_to={'current': True})

    def __str__(self):
        return f"BidRequest {self.bid_id}"