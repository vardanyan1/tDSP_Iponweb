import base64

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


class GameConfigTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_config(self):
        url = reverse("game-configure-list")

        data = {
            "impressions_total": 1,
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
        self.assertEqual(config.budget, data['budget'])


class CampaignTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_campaign(self):
        url = reverse("api-campaign-list")

        # Create config to associate campaign with current config
        config = ConfigModel.objects.create(impressions_total=1000, auction_type=1, mode='free', budget=5000.00,
                                            impression_revenue=0.10, click_revenue=0.50, conversion_revenue=5.00,
                                            frequency_capping=5)
        data = {
            "name": "test campaign",
            "budget": 100,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # check if campaign is created with the correct data
        creative = CampaignModel.objects.get(name=data['name'])
        self.assertEqual(creative.budget, data['budget'])
        self.assertEqual(creative.config, config)


class CreativeTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()

    @staticmethod
    def create_test_image():
        # Create a 100x100 pixel RGB image with a red background
        img = pil.new('RGB', (100, 100), color='red')

        # Encode the image as PNG and get the bytes
        img_bytes = BytesIO()
        img.save(img_bytes, format='PNG')
        img_bytes = img_bytes.getvalue()

        # Encode the image bytes as base64
        encoded_image = base64.b64encode(img_bytes)

        return encoded_image

    def test_create_creative(self):
        url = reverse("api-creative-list")

        # create a campaign and some categories/subcategories for testing
        config = ConfigModel.objects.create(impressions_total=1000, auction_type=1, mode='free', budget=5000.00,
                                            impression_revenue=0.10, click_revenue=0.50, conversion_revenue=5.00,
                                            frequency_capping=5)

        campaign = CampaignModel.objects.create(name='Test Campaign', config=config, budget=500)

        category1 = CategoryModel.objects.create(code='test', tier='tier 1', category="test category")
        category2 = CategoryModel.objects.create(code='test7', tier='tier 1', category="test category")
        subcategory1 = SubcategoryModel.objects.create(code='test2-1', tier='tier 2',
                                                       subcategory="test subcategory", category=category1)
        subcategory2 = SubcategoryModel.objects.create(code='test7-7', tier='tier 2',
                                                       subcategory="test subcategory 2", category=category2)

        image = self.create_test_image()

        data = {
            'external_id': 'external_id',
            'name': 'name',
            'categories': json.dumps([{"code": category1.code}, {"code": subcategory2.code}]),
            'campaign': json.dumps({'id': campaign.id}),
            'file': image,
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # check if creative is created with the correct data
        creative = CreativeModel.objects.get(external_id=data['external_id'])
        self.assertEqual(creative.name, data['name'])
        self.assertEqual(creative.campaign_id, campaign.id)

        # check if categories are added to creative
        self.assertIn(subcategory1, creative.categories.all())
        self.assertIn(subcategory2, creative.categories.all())

        # check if image is saved to separate service and image_url is added to creative
        self.assertTrue(creative.url)

        # creative_url_response = self.client.get(creative.url)
        # self.assertIn('image', creative_url_response['Content-Type']) # TODO: Discuss

        # check if created creative data is returned in the response
        expected_data = {
            'id': creative.id,
            'external_id': data['external_id'],
            'name': data['name'],
            'categories': [{"id": subcategory1.id, "code": subcategory1.code},
                           {"id": subcategory2.id, "code": subcategory2.code}],
            'campaign': {'id': campaign.id, 'name': campaign.name},
            'url': creative.url,
        }

        self.assertEqual(response.data, expected_data)

# class BidViewSetTests(APITestCase):
#     def setUp(self):
#         self.url = reverse('rtb-bid-list')
#         self.user = User.objects.create_user('testuser', password='password')
#         self.client.force_authenticate(user=self.user)
#
#     def test_create_bid_with_valid_data(self):
#         category = CategoryModel.objects.create(code='test', tier='tier 1', category="test category")
#         subcategory = SubcategoryModel.objects.create(code='test-1', tier='tier 1',
#                                                       subcategory="test subcategory", category=category)
#         config = ConfigModel.objects.create(impressions_total=1000, auction_type=1, mode='free', budget=5000.00,
#                                             impression_revenue=0.10, click_revenue=0.50, conversion_revenue=5.00,
#                                             frequency_capping=5)
#
#         data = {
#             'bid_id': 'test_bid_id',
#             'banner_width': 300,
#             'banner_height': 250,
#             'click_probability': 0.5,
#             'conversion_probability': 0.2,
#             'site_domain': 'testsite.com',
#             'ssp_id': 1,
#             'user_id': 'test_user_id',
#             'blocked_categories': [subcategory.id],
#             'config': config,
#         }
#         response = self.client.post(self.url, data)
#
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#         self.assertEqual(BidRequestModel.objects.count(), 1)
#         self.assertEqual(BidResponseModel.objects.count(), 1)
#         self.assertEqual(BidResponseModel.objects.first().external_id, 'test_bid_id')
#         self.assertEqual(BidResponseModel.objects.first().price, 2.50)
#         self.assertEqual(BidResponseModel.objects.first().image_url,
#                          'http://localhost:8001/media/Vek8fPqd8mop5UBpaD7TClRg25kcbflB.jpg')
#         self.assertEqual(BidResponseModel.objects.first().bid_request.banner_width, 300)
#         self.assertEqual(BidResponseModel.objects.first().bid_request.blocked_categories.first().subcategory,
#                          subcategory.subcategory)


# class BidRequestAPITestCase(APITestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.user = User.objects.create_user('testuser', password='password')
#         self.client.force_authenticate(user=self.user)
#
#         self.bid_request_data = {
#             "bid_id": "1234",
#             "banner_width": 100,
#             "banner_height": 200,
#             "click_probability": 0.5,
#             "conversion_probability": 0.3,
#             "site_domain": "example.com",
#             "ssp_id": "1234",
#             "user_id": "5678",
#             "blocked_categories": [],
#         }
#         config = ConfigModel.objects.create(impressions_total=1000, auction_type=1, mode='free', budget=5000.00,
#                                             impression_revenue=0.10, click_revenue=0.50, conversion_revenue=5.00,
#                                             frequency_capping=5)
#
#         category = CategoryModel.objects.create(code='test', tier='tier 1', category="test category")
#         subcategory = SubcategoryModel.objects.create(code='test-1', tier='tier 1',
#                                                       subcategory="test subcategory", category=category)
#         self.bid_request = BidRequestModel.objects.create(
#             bid_id="1234", banner_width=100, banner_height=200, click_probability=0.5, conversion_probability=0.3,
#             site_domain="example.com", ssp_id="1234", user_id="5678", config=config)
#
#         url = reverse("rtb-bid-list")
#         response = self.client.post(url, self.bid_request_data, format="json")
#         self.bid_response = BidResponseModel.objects.last()
#
#     def test_create_bid_request(self):
#
#         url = reverse("rtb-bid-list")
#         response = self.client.post(url, self.bid_request_data, format="json")
#         self.bid_response = BidResponseModel.objects.last()
#
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data["price"], 2.50)
#         self.assertEqual(response.data["image_url"], "http://localhost:8001/media/Vek8fPqd8mop5UBpaD7TClRg25kcbflB.jpg")
#
#     def test_create_notification(self):
#         url = reverse("rtb-notify-list")
#         notification_data = {
#             "bid_id": "1234",
#             "price": 2.50,
#             "win": True,
#             "click": False,
#             "conversion": False,
#             "revenue": 0,
#             "bid_request": self.bid_request.id,
#             "bid_response": self.bid_response.id,
#         }
#         response = self.client.post(url, notification_data, format="json")
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(Notification.objects.count(), 1)
