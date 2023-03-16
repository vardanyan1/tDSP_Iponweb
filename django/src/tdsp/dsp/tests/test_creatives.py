import base64

from PIL import Image as Pil
from io import BytesIO

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from ..models.campaign_model import CampaignModel
from ..models.categories_model import CategoryModel
from ..models.creative_model import CreativeModel
from ..models.game_config_model import ConfigModel


class CreativeTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = reverse("api-creative-list")

        # Create a campaign and some categories for testing
        self.category1 = CategoryModel.objects.create(code='IAB6', name="test category")
        self.category2 = CategoryModel.objects.create(code='IAB6-6', name="test category")

        self.config = ConfigModel.objects.create(
            impressions_total=1000, auction_type=1, mode='free', budget=5000.00,
            impression_revenue=0.10, click_revenue=0.50, conversion_revenue=5.00,
            frequency_capping=5, rounds_left=1000
        )

        self.campaign = CampaignModel.objects.create(name='Free Campaign', config=self.config, budget=100)


    @staticmethod
    def create_test_image():
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
        image = self.create_test_image()

        data = {
            "external_id": "external_id",
            "name": "name",
            "categories": [{"code": self.category1.code}, {"code": self.category2.code}],
            "campaign": {"id": self.campaign.id},
            "file": image,
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # check if creative is created with the correct data
        creative = CreativeModel.objects.get(external_id=data['external_id'])
        self.assertEqual(creative.name, data['name'])
        self.assertEqual(creative.campaign_id, self.campaign.id)

        # check if categories are added to creative
        self.assertIn(self.category1, creative.categories.all())

        # check if image is saved to separate service and image_url is added to creative
        self.assertTrue(creative.url)

        # check if created creative data is returned in the response
        expected_data = {
            'id': creative.id,
            'external_id': data['external_id'],
            'name': data['name'],
            'categories': [{"id": self.category1.id, "code": self.category1.code},
                           {"id": self.category2.id, "code": self.category2.code}],
            'campaign': {'id': self.campaign.id, 'name': self.campaign.name},
            'url': creative.url,
        }

        self.assertEqual(response.data, expected_data)
