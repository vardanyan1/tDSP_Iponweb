from django.db import models
from ..models.bid_request_model import BidRequestModel
from ..models.bid_response_model import BidResponseModel


class NotificationModel(models.Model):
    """
    Represents a notification model in the system.

    Attributes:
        bid_id (str): The ID of the bid associated with the notification.
        price (Decimal): The price of the bid associated with the notification.
        win (bool): Indicates if the bid won the auction.
        click (bool): Indicates if the bid generated a click.
        conversion (bool): Indicates if the bid generated a conversion.
        revenue (int): The revenue generated from the bid.
        bid_request (BidRequestModel): The bid request associated with the notification.
        bid_response (BidResponseModel): The bid response associated with the notification.

    Methods:
        __str__(): Returns a string representation of the NotificationModel instance.
    """
    bid_id = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    win = models.BooleanField()
    click = models.BooleanField(null=True, blank=True)
    conversion = models.BooleanField(null=True, blank=True)
    revenue = models.IntegerField(null=True, blank=True)
    bid_request = models.ForeignKey(BidRequestModel, on_delete=models.CASCADE)
    bid_response = models.ForeignKey(BidResponseModel, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        """
        Returns a string representation of the NotificationModel instance.

        Returns:
            str: A string representing the NotificationModel instance.
        """
        return f"Notification for {self.bid_id} bid"
