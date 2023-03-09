from django.db import models
from ..models.bid_request_model import BidRequestModel
from ..models.categories_model import SubcategoryModel


class BidResponseModel(models.Model):
    external_id = models.CharField(max_length=255)
    price = models.FloatField()
    image_url = models.URLField()
    cat = models.ManyToManyField(SubcategoryModel, blank=True)
    bid_request = models.ForeignKey(BidRequestModel, on_delete=models.CASCADE)

    def __str__(self):
        return f"BidResponse {self.external_id}"
