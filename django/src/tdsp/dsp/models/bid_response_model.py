from django.db import models
from ..models.bid_request_model import BidRequestModel
from ..models.categories_model import CategoryModel


class BidResponseModel(models.Model):
    """
    Represents a bid response in the system.
    """
    external_id = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image_url = models.URLField()
    categories = models.ManyToManyField(CategoryModel, blank=True, related_name="bid_responses")
    bid_request = models.ForeignKey(BidRequestModel, on_delete=models.CASCADE)

    def __str__(self):
        return f"BidResponse {self.external_id}"
