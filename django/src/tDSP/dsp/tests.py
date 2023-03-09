from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile
from ..dsp.models.campaign_model import CampaignModel
from ..dsp.models.creative_model import CreativeModel
from ..dsp.models.categories_model import CategoryModel, SubcategoryModel
from ..dsp.models.game_config_model import ConfigModel
import io


class CreativeViewSetTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()

    def test_create_creative(self):
        url = '/creatives/'
        # create a campaign and some categories/subcategories for testing
        config = ConfigModel.objects.create(impressions_total=1000, auction_type=1, mode='free', budget=5000.00,
                                            impression_revenue=0.10, click_revenue=0.50, conversion_revenue=5.00,
                                            frequency_capping=5)

        campaign = CampaignModel.objects.create(name='Test Campaign', config=config)
        category = CategoryModel.objects.create(IAB_Code='IAB1', Tier='Tier 1', IAB_Category="test category")
        subcategory = SubcategoryModel.objects.create(IAB_Code='IAB1-1', Tier='Tier 1',
                                                      IAB_Subcategory="test subcategory", category=category)

        # create a sample image file
        image_file = io.BytesIO()
        image_file.write(b'example image')
        image_file.seek(0)
        image = SimpleUploadedFile("test_image.jpg", image_file.read(), content_type="image/jpg")

        data = {
            'external_id': '123',
            'name': 'Test Creative',
            'campaign': {'id': campaign.id},
            'categories': [{'code': 'IAB1-1'}],
            'file': image,
        }

        response = self.client.post(url, data, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # check if creative is created with the correct data
        creative = CreativeModel.objects.get(external_id='123')
        self.assertEqual(creative.name, 'Test Creative')
        self.assertEqual(creative.campaign_id, campaign.id)

        # check if categories are added to creative
        self.assertIn(category, creative.categories.all())
        self.assertIn(subcategory, creative.categories.all())

        # check if image is saved to separate service and image_url is added to creative
        self.assertTrue(creative.image_url)

        # check if created creative data is returned in the response
        expected_data = {
            'id': creative.id,
            'external_id': '123',
            'name': 'Test Creative',
            'campaign': {'id': campaign.id, 'name': 'Test Campaign'},
            'categories': [
                {'id': category.id, 'name': 'Test Category', 'code': 'test_cat'},
                {'id': subcategory.id, 'name': 'Test Subcategory', 'code': 'test_cat-1', 'category': category.id},
            ],
            'image_url': creative.image_url,
        }
        self.assertEqual(response.data, expected_data)
