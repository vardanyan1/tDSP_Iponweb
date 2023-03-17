import decimal
import random

from .image_server_tools import send_image, generate_image
from ..dsp.models.campaign_model import CampaignModel
from ..dsp.models.categories_model import CategoryModel
from ..dsp.models.creative_model import CreativeModel
from ..dsp.models.game_config_model import ConfigModel
from ..dsp.models.user_impression_model import UserImpression


def calculate_normalized_weights(budgets):
    """
    Calculate the normalized weights for each creative based on their remaining budget
    """
    total_weight = float(sum(budgets))
    normalized_weights = [float(budget) / total_weight for budget in budgets]

    return normalized_weights


def weighted_random_selection(creatives, budgets):
    """
    Select a creative using a weighted random selection based on the remaining budget
    """
    normalized_weights = calculate_normalized_weights(budgets)
    return random.choices(creatives, weights=normalized_weights, k=1)[0]


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


def calculate_bid_price(bid_request):
    b_categories = bid_request.blocked_categories.all()
    user_id = bid_request.user_id
    click_probability = bid_request.click_probability
    conversion_probability = bid_request.conversion_probability

    config = ConfigModel.objects.get(current=True)
    creatives = CreativeModel.objects.filter(
        campaign__config=config,
        campaign__budget__gt=0
    ).exclude(categories__in=b_categories)

    if not creatives:
        return None, None

    filtered_creatives = [
        creative for creative in creatives
        if (
                   UserImpression.objects.filter(user_id=user_id, campaign_id=creative.campaign_id).first() or
                   UserImpression(impressions=0)
           ).impressions < config.frequency_capping
    ]

    if not filtered_creatives:
        if config.mode == "free":
            create_new_free_campaign_and_creative(config)
            return calculate_bid_price(bid_request)
        else:
            return None, None

    budgets = [creative.campaign.budget for creative in filtered_creatives]
    selected_creative = weighted_random_selection(filtered_creatives, budgets)

    budget_adjustment = selected_creative.campaign.budget / config.rounds_left if\
        config.rounds_left > 0 else selected_creative.campaign.budget

    price = config.impression_revenue + decimal.Decimal(str(click_probability)) * config.click_revenue \
            + decimal.Decimal(str(conversion_probability)) * config.conversion_revenue

    adjusted_price = min(price, budget_adjustment)

    return adjusted_price, selected_creative

