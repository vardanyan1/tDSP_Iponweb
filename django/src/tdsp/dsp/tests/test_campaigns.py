from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from ..models.campaign_model import CampaignModel
from ..models.categories_model import CategoryModel
from ..models.game_config_model import ConfigModel


class CampaignTestCase(APITestCase):
    def setUp(self):
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
            rounds_left=1000
        )

    def test_create_campaign_with_valid_data(self):
        data = {
            "name": "test campaign",
            "budget": 100,
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # check if campaign is created with the correct data
        campaign = CampaignModel.objects.get(name=data['name'])
        self.assertEqual(campaign.budget, data['budget'])
        self.assertEqual(campaign.config, self.config)

    def test_create_campaign_with_missing_name(self):
        data = {
            "budget": 100,
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_campaign_with_missing_budget(self):
        data = {
            "name": "test campaign",
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_campaign_with_negative_budget(self):
        data = {
            "name": "test campaign",
            "budget": -100,
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
