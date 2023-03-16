from django.db import models
from ..models.bid_request_model import BidRequestModel
from ..models.bid_response_model import BidResponseModel


class NotificationModel(models.Model):
    bid_id = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    win = models.BooleanField()
    click = models.BooleanField(null=True, blank=True)
    conversion = models.BooleanField(null=True, blank=True)
    revenue = models.IntegerField(null=True, blank=True)
    bid_request = models.ForeignKey(BidRequestModel, on_delete=models.CASCADE)
    bid_response = models.ForeignKey(BidResponseModel, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Notification for {self.bid_id} bid"
