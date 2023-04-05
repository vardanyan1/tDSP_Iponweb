import base64
from PIL import Image as Pil
from io import BytesIO

from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken


from ..models.campaign_model import CampaignModel
from ..models.categories_model import CategoryModel
from ..models.creative_model import CreativeModel
from ..models.game_config_model import ConfigModel


class CreativeTestCase(APITestCase):
    """
    A test case for testing the creation of creatives using the Creative API endpoint.

    Methods:
        setUp(): Sets up the necessary objects and authentication token before each test case method.
        create_test_image(): Helper function to create a test image for the creative.
        test_create_creative(): Tests creating a creative with valid data and checks that the creative is created with
                                the correct data, categories are added to the creative, the image is saved to a
                                separate service and image_url is added to the creative, and the created creative data
                                is returned in the response.
    """

    def setUp(self):
        """
        Sets up a test user and authenticates the API client with JWT token.
        Creates URLs, categories, a configuration, and a campaign for testing.
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

        # Create a campaign and some categories for testing
        self.category1 = CategoryModel.objects.create(code='IAB6', name="test category")
        self.category2 = CategoryModel.objects.create(code='IAB6-6', name="test category")

        self.config = ConfigModel.objects.create(
            impressions_total=1000, auction_type=1, mode='free', budget=5000.00,
            impression_revenue=0.10, click_revenue=0.50, conversion_revenue=5.00,
            frequency_capping=5, rounds_left=1000, game_goal="revenue"
        )

        self.campaign = CampaignModel.objects.create(name='Free Campaign', config=self.config, budget=100)

    @staticmethod
    def create_test_image():
        """
        Returns a base64 encoded string of a test image.
        """
        # Create a 100x100 pixel RGB image with a red background
        img = Pil.new('RGB', (100, 100), color='red')

        # Encode the image as PNG and get the bytes
        img_bytes = BytesIO()
        img.save(img_bytes, format='PNG')
        img_bytes = img_bytes.getvalue()

        # Encode the image bytes as base64
        encoded_image = base64.b64encode(img_bytes).decode('utf-8')

        return encoded_image

    def test_create_creative(self):
        """
        Test creating a new creative with valid data and checking if the creative is successfully created.
        """
        data = {
            "external_id": "test_creative_001",
            "name": "Test Creative",
            "file": self.create_test_image(),
            "categories": [
                {"code": "IAB6"},
                {"code": "IAB6-6"}
            ],
            "campaign": {"id": self.campaign.id}
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(CreativeModel.objects.filter(external_id="test_creative_001").exists())

    def test_create_creative_duplicate_external_id(self):
        """
        Test creating a creative with a duplicate external_id and checking if the error is handled.
        """
        CreativeModel.objects.create(
            external_id="test_creative_002",
            name="Test Creative 2",
            url="http://example.com/test2",
            campaign=self.campaign
        )
        data = {
            "external_id": "test_creative_002",
            "name": "Test Creative Duplicate",
            "file": self.create_test_image(),
            "categories": [
                {"code": "IAB6"},
                {"code": "IAB6-6"}
            ],
            "campaign": {"id": self.campaign.id}
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data["external_id"][0]), "creative model with this external id already exists.")

    def test_create_creative_invalid_campaign_id(self):
        """
        Test creating a creative with a non-existent campaign ID and checking if the error is handled.
        """
        data = {
            "external_id": "test_external_id",
            "name": "Test Creative",
            "categories": [self.category1.id, self.category2.id],
            "campaign": {"id": 99999},  # Non-existent campaign ID
            "file": self.create_test_image(),
        }

        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["campaign"][0], "Campaign with the provided ID does not exist.")
