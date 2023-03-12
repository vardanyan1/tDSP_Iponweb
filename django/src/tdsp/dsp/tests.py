import base64

from PIL import Image as pil
from io import BytesIO
import json

from django.urls import reverse

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

        category1 = CategoryModel.objects.create(code='test', category="test category")
        category2 = CategoryModel.objects.create(code='test7', category="test category")
        subcategory1 = SubcategoryModel.objects.create(code='test2-1',
                                                       subcategory="test subcategory", category=category1)
        subcategory2 = SubcategoryModel.objects.create(code='test7-7',
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


class BidRequestTests(APITestCase):
    def setUp(self):
        self.url = reverse('rtb-bid-list')

    def test_create_bid_with_valid_data(self):
        config = ConfigModel.objects.create(impressions_total=1000, auction_type=1, mode='free', budget=5000.00,
                                            impression_revenue=0.10, click_revenue=0.50, conversion_revenue=5.00,
                                            frequency_capping=5)

        campaign = CampaignModel.objects.create(name='Test Campaign', config=config, budget=500)

        category1 = CategoryModel.objects.create(code='test', category="test category")
        category2 = CategoryModel.objects.create(code='test7', category="test category")
        subcategory1 = SubcategoryModel.objects.create(code='test2-1',
                                                       subcategory="test subcategory", category=category1)
        subcategory2 = SubcategoryModel.objects.create(code='test7-7',
                                                       subcategory="test subcategory 2", category=category2)

        data = {
            "id": "some_id",
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

                "domain": "www.example.com",
            },
            "ssp": {
                "id": "0938831"
            },

            "user": {
                "id": "u_cq_001_87311"
            },

            "bcat": [
                str(category1.code),
                str(subcategory2.code)
            ],
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that request model created
        self.assertEqual(BidRequestModel.objects.count(), 1)
        # Check that response model created
        self.assertEqual(BidResponseModel.objects.count(), 1)
        # TODO: after creating logic for price change to comparing with real price
        self.assertEqual(BidResponseModel.objects.first().price, 2.50)

        self.assertEqual(BidResponseModel.objects.first().image_url,
                         response.data['image_url'])

        # TODO: add tests for No Bid

    def test_create_notification(self):
        config = ConfigModel.objects.create(impressions_total=1000, auction_type=1, mode='free', budget=5000.00,
                                            impression_revenue=0.10, click_revenue=0.50, conversion_revenue=5.00,
                                            frequency_capping=5)

        campaign = CampaignModel.objects.create(name='Test Campaign', config=config, budget=500)

        category1 = CategoryModel.objects.create(code='test', category="test category")
        category2 = CategoryModel.objects.create(code='test7', category="test category")
        subcategory1 = SubcategoryModel.objects.create(code='test2-1',
                                                       subcategory="test subcategory", category=category1)
        subcategory2 = SubcategoryModel.objects.create(code='test7-7',
                                                       subcategory="test subcategory 2", category=category2)

        creative_url = reverse("api-creative-list")
        creative_data = {
            'external_id': 'external_id',
            'name': 'name',
            'categories': json.dumps([{"code": category1.code}, {"code": subcategory2.code}]),
            'campaign': json.dumps({'id': campaign.id}),
            'file': self.create_test_image(),
        }
        creative_response = self.client.post(creative_url, creative_data, format='json')

        bid_url = reverse("rtb-bid-list")
        bid_data = {
            "id": "some_id",
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

                "domain": "www.example.com",
            },
            "ssp": {
                "id": "0938831"
            },

            "user": {
                "id": "u_cq_001_87311"
            },

            "bcat": [
                str(category1.code),
                str(subcategory2.code)
            ],
        }
        bid_response = self.client.post(bid_url, bid_data, format='json')

        notif_url = reverse("rtb-notify-list")
        notif_data = {
            "id": "some_id",
            "win": True,
            "price": "2.5",
            "click": False,
            "conversion": False,
            "revenue": "5.7"
        }

        notif_response = self.client.post(notif_url, notif_data, format="json")
        self.assertEqual(notif_response.status_code, status.HTTP_200_OK)
        self.assertEqual(Notification.objects.count(), 1)

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
