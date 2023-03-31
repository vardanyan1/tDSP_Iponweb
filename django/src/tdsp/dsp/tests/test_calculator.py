import time

from django.test import TestCase
from ..models.bid_request_model import BidRequestModel
from ..models.campaign_model import CampaignModel
from ..models.categories_model import CategoryModel
from ..models.creative_model import CreativeModel
from ..models.game_config_model import ConfigModel
from ...tools.calculator_v2 import (calculate_bid_price, get_selected_creatives, calculate_expected_revenue,
                                    calculate_bid_amount, create_new_free_campaign_and_creative)


class CalculatorTestCase(TestCase):

    def setUp(self):

        self.config_revenue = ConfigModel.objects.create(
            impressions_total=10, auction_type=1, mode='script', budget=5000.00,
            impression_revenue=0.10, click_revenue=0.50, conversion_revenue=5.00,
            frequency_capping=5, rounds_left=10, game_goal="revenue"
        )
        self.config_cpc = ConfigModel.objects.create(
            impressions_total=10, auction_type=1, mode='script', budget=5000.00,
            impression_revenue=0.10, click_revenue=0.50, conversion_revenue=5.00,
            frequency_capping=5, rounds_left=10, game_goal="cpc"
        )
        self.config_free = ConfigModel.objects.create(
            impressions_total=10, auction_type=1, mode='free', budget=5000.00,
            impression_revenue=0.10, click_revenue=0.50, conversion_revenue=5.00,
            frequency_capping=5, rounds_left=10, game_goal="revenue"
        )

        self.blocked_category = CategoryModel.objects.create(code='IAB6-6', name="test category")
        self.creative_category = CategoryModel.objects.create(code='IAB4-2', name="test category2")
        self.bid_request = BidRequestModel.objects.create(
            banner_width=400, banner_height=300, click_probability=0.5, conversion_probability=0.4,
            site_domain="www.testing_dom", ssp_id="23fd82h3", user_id="test_user2"
        )
        self.bid_request.blocked_categories.set([self.blocked_category])

    def activate_config(self, config_to_activate):
        ConfigModel.objects.filter(current=True).update(current=False)
        config_to_activate.current = True
        config_to_activate.save()

        unique_id = str(time.time())
        self.campaign = CampaignModel.objects.create(
            name=f"test_{unique_id}", budget=5000, config=config_to_activate
        )
        self.creative = CreativeModel.objects.create(
            campaign=self.campaign, external_id=f"test_id_{unique_id}", name="test creative", url="http://test.com"
        )
        self.creative.categories.set([self.creative_category])

    def test_calculate_bid_price(self):
        # Test calculate_bid_price in different game modes and game goals
        self.activate_config(self.config_revenue)
        bid_amount, chosen_creative = calculate_bid_price(self.bid_request)
        self.assertIsNotNone(bid_amount)
        self.assertIsNotNone(chosen_creative)

        self.activate_config(self.config_cpc)
        bid_amount, chosen_creative = calculate_bid_price(self.bid_request)
        self.assertIsNotNone(bid_amount)
        self.assertIsNotNone(chosen_creative)

        self.activate_config(self.config_free)
        bid_amount, chosen_creative = calculate_bid_price(self.bid_request)
        self.assertIsNotNone(bid_amount)
        self.assertIsNotNone(chosen_creative)

    def test_get_selected_creatives(self):
        # Test get_selected_creatives with different game modes and blocked categories
        self.activate_config(self.config_revenue)
        selected_creatives = get_selected_creatives(self.config_revenue, [self.blocked_category])
        self.assertEqual(len(selected_creatives), 1)
        self.assertEqual(selected_creatives[0], self.creative)

        self.activate_config(self.config_cpc)
        selected_creatives = get_selected_creatives(self.config_cpc, [self.blocked_category])
        self.assertEqual(len(selected_creatives), 1)
        self.assertEqual(selected_creatives[0], self.creative)

        self.activate_config(self.config_free)
        selected_creatives = get_selected_creatives(self.config_free, [self.blocked_category])
        self.assertEqual(len(selected_creatives), 1)
        self.assertEqual(selected_creatives[0], self.creative)

    def test_calculate_expected_revenue(self):
        # Test calculate_expected_revenue with different game goals
        expected_revenue = calculate_expected_revenue(self.bid_request, self.config_revenue)
        self.assertIsInstance(expected_revenue, float)

        expected_revenue = calculate_expected_revenue(self.bid_request, self.config_cpc)
        self.assertIsInstance(expected_revenue, float)

    def test_calculate_bid_amount(self):
        self.activate_config(self.config_revenue)
        # Test calculate_bid_amount with different budgets, rounds left, and expected revenues
        rounds_left = 10
        expected_revenue = 10

        bid_amount = calculate_bid_amount(expected_revenue, self.creative.campaign, rounds_left)
        self.assertEqual(bid_amount, expected_revenue)

        rounds_left = 5
        expected_revenue = 30

        bid_amount = calculate_bid_amount(expected_revenue, self.creative.campaign, rounds_left)
        self.assertEqual(bid_amount, 30)

    def test_create_new_free_campaign_and_creative(self):
        self.activate_config(self.config_free)

        # Create a new free campaign and creative
        new_creative = create_new_free_campaign_and_creative(self.config_free)

        # Test if the new creative is created with correct properties
        self.assertIsNotNone(new_creative)
        self.assertEqual(new_creative.external_id, "new_free_creative_id")
        self.assertEqual(new_creative.name, "New Free Creative")
        self.assertEqual(new_creative.url, new_creative.url)
        self.assertEqual(new_creative.campaign.config, self.config_free)
        self.assertEqual(new_creative.categories.first().code, "IAB6-6")
