from PIL import Image as pil
from io import BytesIO
import json

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from ..dsp.models.campaign_model import CampaignModel
from ..dsp.models.creative_model import CreativeModel
from ..dsp.models.categories_model import CategoryModel, SubcategoryModel
from ..dsp.models.game_config_model import ConfigModel


class CreativeViewSetTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user('testuser', password='password')
        self.client.force_authenticate(user=self.user)

    @staticmethod
    def create_test_image():
        # Create a 100x100 pixel RGB image with a red background
        img = pil.new('RGB', (100, 100), color='red')
        # Save the image to a byte stream
        stream = BytesIO()
        img.save(stream, format='PNG')
        # Return the byte stream content as bytes
        return stream.getvalue()

    def test_create_creative(self):
        url = 'http://localhost:8000/api/creatives/'
        # create a campaign and some categories/subcategories for testing
        config = ConfigModel.objects.create(impressions_total=1000, auction_type=1, mode='free', budget=5000.00,
                                            impression_revenue=0.10, click_revenue=0.50, conversion_revenue=5.00,
                                            frequency_capping=5)

        campaign = CampaignModel.objects.create(name='Test Campaign', config=config, budget=500)
        category = CategoryModel.objects.create(IAB_Code='test', Tier='Tier 1', IAB_Category="test category")
        subcategory = SubcategoryModel.objects.create(IAB_Code='test-1', Tier='Tier 1',
                                                      IAB_Subcategory="test subcategory", category=category)

        image = SimpleUploadedFile("test_image.jpg", self.create_test_image(), content_type="image/jpg")

        data = {
            'external_id': '123',
            'name': 'Test Creative',
            'categories': json.dumps([{'code': category.IAB_Code}]),
            'campaign': json.dumps({'id': campaign.id}),
            'file': image,
        }

        response = self.client.post(url, data, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # check if creative is created with the correct data
        creative = CreativeModel.objects.get(external_id='123')
        self.assertEqual(creative.name, 'Test Creative')
        self.assertEqual(creative.campaign_id, campaign.id)

        # check if categories are added to creative
        self.assertIn(subcategory, creative.categories.all())

        # check if image is saved to separate service and image_url is added to creative
        self.assertTrue(creative.url)

        # check if created creative data is returned in the response
        expected_data = {
            'id': creative.id,
            'external_id': '123',
            'name': 'Test Creative',
            'categories': [{'id': subcategory.id, 'code': subcategory.IAB_Code}],
            'campaign': {'id': campaign.id, 'name': campaign.name},
            'url': creative.url,
        }
        self.assertEqual(response.data, expected_data)
