from django.db import models
from ..models.game_config_model import ConfigModel
from ..models.categories_model import SubcategoryModel


class BidRequestModel(models.Model):
    bid_id = models.CharField(max_length=255)
    banner_width = models.IntegerField()
    banner_height = models.IntegerField()
    click_probability = models.FloatField()
    conversion_probability = models.FloatField()
    site_domain = models.CharField(max_length=255)
    ssp_id = models.CharField(max_length=255)
    user_id = models.CharField(max_length=255)
    blocked_categories = models.ManyToManyField(SubcategoryModel, blank=True)
    config = models.ForeignKey(ConfigModel, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"BidRequest {self.bid_id}"
