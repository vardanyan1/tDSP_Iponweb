from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from ..models.categories_model import CategoryModel
from ..models.game_config_model import ConfigModel


class GameConfigTestCase(APITestCase):
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

    def test_create_free_game_mode_config(self):
        url = reverse("game-configure-list")

        CategoryModel.objects.create(code="IAB6-6", name="test category")

        data = {
            "impressions_total": 3,
            "auction_type": 2,
            "mode": "free",
            "budget": 1000,
            "impression_revenue": 10,
            "click_revenue": 20,
            "conversion_revenue": 30,
            "frequency_capping": None,
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # check if config is created with the correct data
        config = ConfigModel.objects.get(current=True)
        self.assertEqual(config.auction_type, data['auction_type'])
        if config.mode == "free":
            self.assertEqual(config.budget, 0)
        else:
            self.assertEqual(config.budget, data['budget'])
        self.assertEqual(config.rounds_left, data['impressions_total'])

        # TODO Add test for free and script separately
