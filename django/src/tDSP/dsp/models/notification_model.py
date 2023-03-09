from django.db import models
from ..models.bid_request_model import BidRequestModel
from ..models.bid_response_model import BidResponseModel


class Notification(models.Model):
    bid_id = models.CharField(max_length=255)
    price = models.FloatField()
    win = models.BooleanField()
    click = models.BooleanField()
    conversion = models.BooleanField()
    revenue = models.FloatField()
    bid_request = models.ForeignKey(BidRequestModel, on_delete=models.CASCADE)
    bid_response = models.ForeignKey(BidResponseModel, on_delete=models.CASCADE)

    def __str__(self):
        return f"Notification for {self.bid_id} bid"
    