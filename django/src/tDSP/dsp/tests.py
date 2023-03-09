from PIL import Image as pil
from io import BytesIO
import json

from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from .models.bid_request_model import BidRequestModel
from .models.bid_response_model import BidResponseModel
from .models.notification_model import Notification
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
        category = CategoryModel.objects.create(code='test', tier='tier 1', category="test category")
        subcategory = SubcategoryModel.objects.create(code='test-1', tier='tier 1',
                                                      subcategory="test subcategory", category=category)

        image = SimpleUploadedFile("test_image.jpg", self.create_test_image(), content_type="image/jpg")

        data = {
            'external_id': '123',
            'name': 'Test Creative',
            'categories': json.dumps([{'code': category.code}]),
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
            'categories': [{'id': subcategory.id, 'code': subcategory.code}],
            'campaign': {'id': campaign.id, 'name': campaign.name},
            'url': creative.url,
        }
        self.assertEqual(response.data, expected_data)


class BidViewSetTests(APITestCase):
    def setUp(self):
        self.url = reverse('rtb-bid-list')
        self.user = User.objects.create_user('testuser', password='password')
        self.client.force_authenticate(user=self.user)

    def test_create_bid_with_valid_data(self):
        category = CategoryModel.objects.create(code='test', tier='tier 1', category="test category")
        subcategory = SubcategoryModel.objects.create(code='test-1', tier='tier 1',
                                                      subcategory="test subcategory", category=category)
        config = ConfigModel.objects.create(impressions_total=1000, auction_type=1, mode='free', budget=5000.00,
                                            impression_revenue=0.10, click_revenue=0.50, conversion_revenue=5.00,
                                            frequency_capping=5)

        data = {
            'bid_id': 'test_bid_id',
            'banner_width': 300,
            'banner_height': 250,
            'click_probability': 0.5,
            'conversion_probability': 0.2,
            'site_domain': 'testsite.com',
            'ssp_id': 1,
            'user_id': 'test_user_id',
            'blocked_categories': [subcategory.id],
            'config': config,
        }
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(BidRequestModel.objects.count(), 1)
        self.assertEqual(BidResponseModel.objects.count(), 1)
        self.assertEqual(BidResponseModel.objects.first().external_id, 'test_bid_id')
        self.assertEqual(BidResponseModel.objects.first().price, 2.50)
        self.assertEqual(BidResponseModel.objects.first().image_url,
                         'http://localhost:8001/media/Vek8fPqd8mop5UBpaD7TClRg25kcbflB.jpg')
        self.assertEqual(BidResponseModel.objects.first().bid_request.banner_width, 300)
        self.assertEqual(BidResponseModel.objects.first().bid_request.blocked_categories.first().subcategory,
                         subcategory.subcategory)


class BidRequestAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user('testuser', password='password')
        self.client.force_authenticate(user=self.user)

        self.bid_request_data = {
            "bid_id": "1234",
            "banner_width": 100,
            "banner_height": 200,
            "click_probability": 0.5,
            "conversion_probability": 0.3,
            "site_domain": "example.com",
            "ssp_id": "1234",
            "user_id": "5678",
            "blocked_categories": [],
        }
        config = ConfigModel.objects.create(impressions_total=1000, auction_type=1, mode='free', budget=5000.00,
                                            impression_revenue=0.10, click_revenue=0.50, conversion_revenue=5.00,
                                            frequency_capping=5)

        category = CategoryModel.objects.create(code='test', tier='tier 1', category="test category")
        subcategory = SubcategoryModel.objects.create(code='test-1', tier='tier 1',
                                                      subcategory="test subcategory", category=category)
        self.bid_request = BidRequestModel.objects.create(
            bid_id="1234", banner_width=100, banner_height=200, click_probability=0.5, conversion_probability=0.3,
            site_domain="example.com", ssp_id="1234", user_id="5678", config=config)

        url = reverse("rtb-bid-list")
        response = self.client.post(url, self.bid_request_data, format="json")
        self.bid_response = BidResponseModel.objects.last()

    def test_create_bid_request(self):

        url = reverse("rtb-bid-list")
        response = self.client.post(url, self.bid_request_data, format="json")
        self.bid_response = BidResponseModel.objects.last()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["price"], 2.50)
        self.assertEqual(response.data["image_url"], "http://localhost:8001/media/Vek8fPqd8mop5UBpaD7TClRg25kcbflB.jpg")

    def test_create_notification(self):
        url = reverse("rtb-notify-list")
        notification_data = {
            "bid_id": "1234",
            "price": 2.50,
            "win": True,
            "click": False,
            "conversion": False,
            "revenue": 0,
            "bid_request": self.bid_request.id,
            "bid_response": self.bid_response.id,
        }
        response = self.client.post(url, notification_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Notification.objects.count(), 1)
