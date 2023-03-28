from django.db.models import Q
from typing import Optional, Tuple, List

from .ads_txt_check import ssp_check
from .image_server_tools import send_image, generate_image
from ..dsp.models.bid_request_model import BidRequestModel
from ..dsp.models.campaign_model import CampaignModel
from ..dsp.models.categories_model import CategoryModel
from ..dsp.models.creative_model import CreativeModel
from ..dsp.models.game_config_model import ConfigModel
from ..dsp.models.user_impression_model import UserImpression


def calculate_bid_price(bid_request: BidRequestModel) -> Tuple[Optional[float], Optional[CreativeModel]]:
    """
    Calculates the bid price for a given bid request.

    :param bid_request: (BidRequest) The bid request for which to calculate the bid price.

    :return Tuple[Optional[float], Optional[CreativeModel]]: The chosen bid amount and chosen creative.
    """
    b_categories = bid_request.blocked_categories.all()
    game_config = ConfigModel.objects.get(current=True)
    user_id = bid_request.user_id

    # Get selected creatives based on game mode
    selected_creatives = get_selected_creatives(game_config, b_categories)
    if not selected_creatives:
        return None, None

    # Filter out creatives based on frequency_capping
    filtered_creatives = [
        creative for creative in selected_creatives
        if (
                   UserImpression.objects.filter(user_id=user_id, campaign_id=creative.campaign_id).first() or
                   UserImpression(impressions=0)
           ).impressions < game_config.frequency_capping
    ]

    # If there's no filtered creative, and it's a free mode game, create new campaign and creative
    if not filtered_creatives:
        if game_config.mode == "free":
            create_new_free_campaign_and_creative(game_config)
            return calculate_bid_price(bid_request)
        else:
            return None, None

    # Calculate expected revenue
    expected_revenue = calculate_expected_revenue(bid_request, game_config)

    # Calculate the bid amount for each filtered creative
    bid_amounts = [
        calculate_bid_amount(
            expected_revenue,
            float(creative.campaign.budget),
            game_config.rounds_left
        )
        for creative in filtered_creatives
    ]

    # Choose the creative with the highest bid amount
    max_bid_amount_index = bid_amounts.index(max(bid_amounts))
    chosen_creative = filtered_creatives[max_bid_amount_index]
    chosen_bid_amount = bid_amounts[max_bid_amount_index]

    return chosen_bid_amount, chosen_creative


def get_selected_creatives(game_config: ConfigModel, b_categories: List[CategoryModel]) -> List[CreativeModel]:
    """
    Retrieves the selected creatives based on the game configuration and blocked categories.

    :param game_config: (ConfigModel) The game configuration.
    :param b_categories: (List[CategoryModel]) The list of blocked categories.

    :return List[CreativeModel]: The list of selected creatives.
    """
    if game_config.mode == "free":
        # Select the appropriate creative
        selected_creatives = CreativeModel.objects.filter(
            campaign__config=game_config,
            campaign__budget__gt=0
        )
    elif game_config.mode == "script":
        # Create a Q object to match creatives with blocked parent categories or subcategories
        blocked_categories_query = Q()
        for b_category in b_categories:
            blocked_categories_query |= Q(categories=b_category) | Q(categories__parent=b_category)

        # Select the appropriate creative
        selected_creatives = CreativeModel.objects.filter(
            campaign__config=game_config,
            campaign__budget__gt=0
        ).exclude(blocked_categories_query)

    else:
        raise ValueError("Invalid game mode")

    return selected_creatives


def calculate_expected_revenue(bid_request: BidRequestModel, game_config: ConfigModel) -> float:
    """
    Calculates the expected revenue for a given bid request and game configuration.

    :param bid_request: (BidRequest) The bid request for which to calculate the expected revenue.
    :param game_config: (ConfigModel) The game configuration.

    :return float: The expected revenue.
    """
    if game_config.game_goal == "revenue":
        # SSP Ads.txt check
        if ssp_check(bid_request.ssp_id, bid_request.site_domain):
            impression_revenue = float(game_config.impression_revenue)
        else:
            impression_revenue = 0
        click_revenue = float(game_config.click_revenue) * bid_request.click_probability
        conversion_revenue = float(game_config.conversion_revenue) * bid_request.conversion_probability
        expected_revenue = click_revenue + conversion_revenue + impression_revenue
    elif game_config.game_goal == "cpc":
        expected_revenue = float(game_config.click_revenue) * bid_request.click_probability
    else:
        raise ValueError("Invalid game goal")

    return expected_revenue


def calculate_bid_amount(expected_revenue, budget, rounds_left):
    """
    Calculates the bid amount based on the expected revenue, budget, and remaining rounds.

    :param    expected_revenue: (float) The expected revenue for the bid.
    :param    budget: (float) The remaining budget for the campaign.
    :param    rounds_left: (int) The number of rounds left in the auction.

    :return float: The calculated bid amount.
    """
    # Calculate the average budget per round
    budget_per_round = budget / rounds_left

    # Calculate the bid amount
    bid_amount = min(expected_revenue, budget_per_round)

    return bid_amount


def create_new_free_campaign_and_creative(config):
    """
    Create a new free campaign and creative, and return the creative
    """
    old_campaign = CampaignModel.objects.filter(config=config).first()
    old_campaign_budget = 0
    if old_campaign:
        old_campaign_budget = old_campaign.budget
        old_campaign.delete()

    campaign = CampaignModel.objects.create(
        name='New Free Campaign', config=config, budget=old_campaign_budget
    )

    image_url = send_image(generate_image(300, 200))
    creative = CreativeModel.objects.create(
        external_id="new_free_creative_id", name="New Free Creative",
        campaign_id=campaign.id, url=image_url
    )
    category = CategoryModel.objects.get(code="IAB6-6")
    creative.categories.add(category)

    return creative
