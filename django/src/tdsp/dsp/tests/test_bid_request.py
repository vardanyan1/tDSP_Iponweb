from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from ..models.bid_request_model import BidRequestModel
from ..models.bid_response_model import BidResponseModel
from ..models.campaign_model import CampaignModel
from ..models.categories_model import CategoryModel
from ..models.game_config_model import ConfigModel
from ...tools.image_server_tools import generate_image


class BidRequestTests(APITestCase):
    """
    Test case for the Bid Request API.

    Methods:
        setUp(): Initializes the test case with test data.
        test_create_bid_with_valid_data(): Tests creating a bid with valid data.
    """
    def setUp(self):
        """
        Initializes the test case with test data.
        """
        # Create a test user
        self.test_user = User.objects.create_user(
            username='test',
            password='test'
        )
        # Get JWT token and use in headers
        refresh = RefreshToken.for_user(self.test_user)
        self.token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

        self.bid_request_url = reverse('rtb-bid-list')
        self.creative_url = reverse("api-creative-list")

        self.category1 = CategoryModel.objects.create(code='IAB6', name="test category")
        self.category2 = CategoryModel.objects.create(code='test7', name="test category")

        self.config = ConfigModel.objects.create(
            impressions_total=10, auction_type=1, mode='free', budget=5000.00,
            impression_revenue=0.10, click_revenue=0.50, conversion_revenue=5.00,
            frequency_capping=5, rounds_left=10, game_goal="revenue"
        )

        self.campaign = CampaignModel.objects.create(name='Test Campaign', config=self.config, budget=500)

    def test_create_bid_with_valid_data(self):
        """
        Tests creating a bid with valid data.
        """
        image = generate_image(300, 400)
        creative_data = {
            "external_id": "external_id_creative1",
            "name": "name",
            "categories": [{"code": self.category2.code}],
            "campaign": {"id": self.campaign.id},
            "file": image,
        }

        creative_response = self.client.post(self.creative_url, creative_data, format='json')

        bid_request_data = {
            "id": "some_id1",
            "imp": {
                "banner": {
                    "w": 300,
                    "h": 250
                },
            },
            "click": {
                "prob": "0.1"
            },
            "conv": {
                "prob": "0.89"
            },
            "site": {
                "domain": "www.example.com"
            },
            "ssp": {
                "id": "none"
            },
            "user": {
                "id": "u_cq_001_87311"
            },
            "bcat": [
                str(self.category1.code)
            ]
        }

        response = self.client.post(self.bid_request_url, bid_request_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that request model created
        self.assertEqual(BidRequestModel.objects.count(), 1)
        # Check that response model created
        self.assertEqual(BidResponseModel.objects.count(), 1)

        # self.assertEqual(BidResponseModel.objects.first().price, 2.50)

        self.assertEqual(
            f"{BidResponseModel.objects.first().image_url}?w={bid_request_data['imp']['banner']['w']}"
            f"&h={bid_request_data['imp']['banner']['h']}",
            response.data['image_url'])

    def test_bid_request_no_appropriate_creative(self):
        """
        Ensure that a bid request returns a no-bid response when there is no appropriate creative available.
        """
        # Create a bid request with a non-existent category in the 'bcat' field
        bid_request_data = {
            "id": "some_id1",
            "imp": {
                "banner": {
                    "w": 300,
                    "h": 250
                },
            },
            "click": {
                "prob": "0.1"
            },
            "conv": {
                "prob": "0.89"
            },
            "site": {
                "domain": "www.example.com"
            },
            "ssp": {
                "id": "none"
            },
            "user": {
                "id": "u_cq_001_87311"
            },
            "bcat": [
                str(self.category1.code),
                str(self.category2.code)
            ]
        }

        response = self.client.post(self.bid_request_url, bid_request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_bid_request_zero_bid_price(self):
        """
        Ensure that a bid request returns a no-bid response when the bid price is zero.
        """
        # Create a bid request with very low probabilities, so the bid price is zero
        bid_request_data = {
            "id": "some_id1",
            "imp": {
                "banner": {
                    "w": 300,
                    "h": 250
                },
            },
            "click": {
                "prob": "0.0001"
            },
            "conv": {
                "prob": "0.0001"
            },
            "site": {
                "domain": "www.example.com"
            },
            "ssp": {
                "id": "none"
            },
            "user": {
                "id": "u_cq_001_87311"
            },
            "bcat": [
                str(self.category1.code),
                str(self.category2.code)
            ]
        }

        response = self.client.post(self.bid_request_url, bid_request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_bid_request_no_rounds_left(self):
        """
        Ensure that a bid request returns an error when the game has no rounds left.
        """
        # Set the rounds_left to 0
        self.config.rounds_left = 0
        self.config.save()

        bid_request_data = {
            "id": "some_id1",
            "imp": {
                "banner": {
                    "w": 300,
                    "h": 250
                },
            },
            "click": {
                "prob": "0.1"
            },
            "conv": {
                "prob": "0.89"
            },
            "site": {
                "domain": "www.example.com"
            },
            "ssp": {
                "id": "none"
            },
            "user": {
                "id": "u_cq_001_87311"
            },
            "bcat": [
                str(self.category1.code)
            ]
        }

        response = self.client.post(self.bid_request_url, bid_request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"error": "No rounds left."})
