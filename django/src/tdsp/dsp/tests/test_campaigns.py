from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from ..models.campaign_model import CampaignModel
from ..models.categories_model import CategoryModel
from ..models.game_config_model import ConfigModel


class CampaignTestCase(APITestCase):
    """
    A test case for testing the creation of campaigns using the Campaign API endpoint.

    Methods:
        setUp(): Sets up the necessary objects and authentication token before each test case method.
        test_create_campaign_with_valid_data(): Tests creating a campaign with valid data and checks that the campaign
                                                  is created with the correct data.
        test_create_campaign_with_missing_name(): Tests creating a campaign with missing name field and expects an
                                                  HTTP 400 error response.
        test_create_campaign_with_missing_budget(): Tests creating a campaign with missing budget field and expects an
                                                    HTTP 400 error response.
        test_create_campaign_with_negative_budget(): Tests creating a campaign with a negative budget value and
                                                      expects an HTTP 400 error response.
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

        self.url = reverse("api-campaign-list")

        self.category = CategoryModel.objects.create(code="IAB6-6", name="test category")

        self.config = ConfigModel.objects.create(
            impressions_total=10,
            auction_type=1,
            mode='free',
            budget=5000.00,
            impression_revenue=0.10,
            click_revenue=0.50,
            conversion_revenue=5.00,
            frequency_capping=5,
            rounds_left=1000,
            game_goal="revenue"
        )

    def test_create_campaign_with_valid_data(self):
        """
        Tests creating a campaign with valid data and checks that the campaign is created with the correct data.
        """
        data = {
            "name": "Test Campaign",
            "budget": 1000.00,
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CampaignModel.objects.count(), 1)

    def test_update_campaign(self):
        """
        Tests the campaign update process.
        """
        campaign = CampaignModel.objects.create(name="Test Campaign", budget=1000.00, config=self.config)
        url = reverse("api-campaign-detail", kwargs={"pk": campaign.pk})
        data = {
            "name": "Updated Campaign",
            "budget": 1200.00,
        }

        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Updated Campaign")
        self.assertEqual(response.data["budget"], 1200)

    def test_create_campaign_with_negative_budget(self):
        """
        Tests the campaign creation process with a negative budget.
        """
        data = {
            "name": "Test Campaign",
            "budget": -1000.00,
            "is_active": True,
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
        self.assertEqual(response.data["error"][0], "Budget must be non-negative.")

    def test_create_campaign_with_insufficient_budget(self):
        """
        Tests the campaign creation process with an insufficient budget in the current game configuration.
        """
        data = {
            "name": "Test Campaign",
            "budget": 6000.00,
            "is_active": True,
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
        self.assertEqual(response.data["error"][0], "Budget is insufficient to create the campaign.")

    def test_create_campaign_without_current_config(self):
        """
        Tests the campaign creation process without a current game configuration.
        """
        self.config.delete()  # Remove the current game configuration
        data = {
            "name": "Test Campaign",
            "budget": 1000.00,
            "is_active": True,
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
        self.assertEqual(response.data["error"][0], "No current game configuration found.")

