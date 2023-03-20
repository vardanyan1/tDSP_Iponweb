from django.db import models
from ..models.bid_request_model import BidRequestModel
from ..models.categories_model import CategoryModel


class BidResponseModel(models.Model):
    """
    Represents a bid response in the system.

    Attributes:
        external_id (str): The external ID of the bid response.
        price (Decimal): The price of the bid response.
        image_url (str): The URL of the image associated with the bid response.
        categories (ManyToManyField): A many-to-many relationship with the CategoryModel, representing the categories
            associated with the bid response.
        bid_request (ForeignKey): A foreign key relationship with the BidRequestModel, representing the bid request
            associated with the bid response.

    Methods:
        __str__(): Returns a string representation of the BidResponseModel instance.
    """
    external_id = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image_url = models.URLField()
    categories = models.ManyToManyField(CategoryModel, blank=True, related_name="bid_responses")
    bid_request = models.ForeignKey(BidRequestModel, on_delete=models.CASCADE)

    def __str__(self) -> str:
        """
        Returns a string representation of the BidResponseModel instance.

        Returns:
            str: A string representing the BidResponseModel instance.
        """
        return f"BidResponse {self.external_id}"
