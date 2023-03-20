from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from ..models.bid_request_model import BidRequestModel
from ..models.bid_response_model import BidResponseModel
from ..models.campaign_model import CampaignModel
from ..models.categories_model import CategoryModel
from ..models.creative_model import CreativeModel
from ..models.game_config_model import ConfigModel
from ..models.notification_model import NotificationModel
from ..models.user_impression_model import UserImpression
from ...tools.image_server_tools import generate_image


class NotificationTests(APITestCase):
    """
    A test case for testing the Notification API endpoint.

    Methods:
        setUp(): Sets up the necessary objects and authentication token before each test case method.
        test_create_notification(): Tests creating a notification object by simulating the creation of all necessary
                                    objects and checking that the notification object and user impression are
                                    created correctly.
        test_create_no_bid_notification(): Tests creating a notification object with no bid response by simulating
                                            the creation of a bid request and checking that the notification object is
                                            created correctly but no user impression is added.
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

        self.url = reverse("api-creative-list")
        self.bid_request_url = reverse('rtb-bid-list')
        self.notification_url = reverse("rtb-notify-list")
        self.creative_url = reverse("api-creative-list")

        self.config = ConfigModel.objects.create(
            impressions_total=10, auction_type=1, mode='free', budget=5000.00,
            impression_revenue=0.10, click_revenue=0.50, conversion_revenue=5.00,
            frequency_capping=5, rounds_left=10, game_goal="revenue"
        )

        self.campaign = CampaignModel.objects.create(name='Test Campaign', config=self.config, budget=500)

        self.category1 = CategoryModel.objects.create(code='IAB6', name="test category")
        self.category2 = CategoryModel.objects.create(code='test7', name="test category")

    def test_create_notification(self):
        """
        Tests creating a notification for bid with valid data.
        """
        # Create Creative
        image = generate_image(300, 300)
        creative_data = {
            "external_id": "external_id_creative1",
            "name": "name",
            "categories": [{"code": self.category2.code}],
            "campaign": {"id": self.campaign.id},
            "file": image,
        }
        self.client.post(self.creative_url, creative_data, format='json')

        # Create Bid Request
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
                "id": "0938831"
            },
            "user": {
                "id": "u_cq_001_87311"
            },
            "bcat": [
                str(self.category1.code)
            ]
        }
        bid_response = self.client.post(self.bid_request_url, bid_request_data, format='json')
        bid_request = BidRequestModel.objects.first()
        bid_response_obj = BidResponseModel.objects.first()

        # Create Notification
        notification_data = {
            "id": bid_request.bid_id,
            "win": True,
            "price": 10
        }
        notification_response = self.client.post(self.notification_url, notification_data, format='json')

        self.assertEqual(notification_response.status_code, status.HTTP_200_OK)

        # Check that notification model created
        self.assertEqual(NotificationModel.objects.count(), 1)
        notification = NotificationModel.objects.first()
        self.assertEqual(notification.bid_id, bid_request.bid_id)
        self.assertEqual(notification.bid_request, bid_request)
        self.assertEqual(notification.bid_response, bid_response_obj)

        # Check UserImpression update
        user_impression = UserImpression.objects.first()
        self.assertEqual(user_impression.user_id, bid_request.user_id)
        self.assertEqual(user_impression.impressions, 1)

        related_creative = CreativeModel.objects.get(external_id=bid_response_obj.external_id)
        self.assertEqual(user_impression.campaign, related_creative.campaign)

    def test_create_no_bid_notification(self):
        """
        Tests checking that the notification object with win=False
        is created correctly but no user impression is added.
        """
        # Create Bid Request
        bid_request_data = {
            "id": "some_id2",
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
                "id": "0938832"
            },
            "user": {
                "id": "u_cq_001_87312"
            },
            "bcat": [
                str(self.category1.code)
            ]
        }
        self.client.post(self.bid_request_url, bid_request_data, format='json')
        bid_request = BidRequestModel.objects.get(bid_id="some_id2")

        # Create Notification
        notification_data = {
            "id": bid_request.bid_id,
            "win": False,
        }
        notification_response = self.client.post(self.notification_url, notification_data, format='json')

        self.assertEqual(notification_response.status_code, status.HTTP_200_OK)

        # Check that notification model created
        self.assertEqual(NotificationModel.objects.count(), 1)
        notification = NotificationModel.objects.first()
        self.assertEqual(notification.bid_id, bid_request.bid_id)
        self.assertEqual(notification.bid_request, bid_request)
        self.assertIsNone(notification.bid_response)

        # Check that UserImpression is not updated
        user_impression_count = UserImpression.objects.count()
        self.assertEqual(user_impression_count, 0)
