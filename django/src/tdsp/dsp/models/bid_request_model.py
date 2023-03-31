from django.db import models
from ..models.game_config_model import ConfigModel
from ..models.categories_model import CategoryModel


class BidRequestModel(models.Model):
    """
    Represents a bid request in the system.

    Attributes:
        bid_id (str): A unique identifier for the bid request.
        banner_width (int): The width of the requested banner.
        banner_height (int): The height of the requested banner.
        click_probability (float): The probability of a user clicking on the banner.
        conversion_probability (float): The probability of a user converting after clicking on the banner.
        site_domain (str): The domain of the site making the request.
        ssp_id (str): The ID of the supply-side platform making the request.
        user_id (str): The ID of the user making the request.
        blocked_categories (ManyToManyField): The categories that are blocked for this bid request.
        config (ForeignKey): The current game configuration object.

    Methods:
        __str__(): Returns a string representation of the BidResponseModel instance.
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
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        """
        Returns a string representation of the BidRequestModel instance.

        Returns:
            str: A string representing the BidResponseModel instance.
        """
        return f"BidRequest:{self.bid_id}"
