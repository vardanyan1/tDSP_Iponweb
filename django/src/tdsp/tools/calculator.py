import decimal
import random
from django.db.models import Q

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
    selected_creative = random.choices(creatives, weights=normalized_weights, k=1)[0]

    return selected_creative


def calculate_bid_price(bid_request):
    b_categories = bid_request.blocked_categories.all()
    user_id = bid_request.user_id
    click_probability = bid_request.click_probability
    conversion_probability = bid_request.conversion_probability

    config = ConfigModel.objects.get(current=True)
    creatives = CreativeModel.objects.filter(
        Q(campaign__config=config) &
        ~Q(categories__in=b_categories) &
        Q(campaign__budget__gt=0)
    )

    if not creatives:
        return None, None

    # Fetch UserImpression instances for the given user and campaigns in a single query
    user_impressions = UserImpression.objects.filter(user_id=user_id, campaign__in=creatives.values('campaign'))

    # Create a dictionary to map campaign id to impressions
    campaign_impressions = {user_impression.campaign_id: user_impression.impressions for user_impression in
                            user_impressions}

    # Filter creatives based on the fetched UserImpression instances
    filtered_creatives = [
        creative for creative in creatives
        if campaign_impressions.get(creative.campaign_id, 0) < config.frequency_capping
    ]

    if not filtered_creatives:
        # Check if the game mode is free
        if config.mode == "free":
            # Delete the old campaign and get its budget
            old_campaign = CampaignModel.objects.filter(config=config).first()
            old_campaign_budget = 0
            if old_campaign:
                old_campaign_budget = old_campaign.budget
                old_campaign.delete()

            # Create a new campaign with the old campaign's budget
            campaign = CampaignModel.objects.create(name='New Free Campaign', config=config, budget=old_campaign_budget)

            # Create a new creative
            image_url = send_image(generate_image(300, 200))
            creative = CreativeModel.objects.create(external_id="new_free_creative_id", name="New Free Creative",
                                                    campaign_id=campaign.id, url=image_url)
            category = CategoryModel.objects.get(code="IAB6-6")
            creative.categories.add(category)

            # Use the newly created creative to calculate again
            return calculate_bid_price(bid_request)
        else:
            return None, None

    budgets = [creative.campaign.budget for creative in filtered_creatives]
    selected_creative = weighted_random_selection(filtered_creatives, budgets)

    # Calculate the price adjustment factor based on the remaining budget and rounds left
    budget_adjustment = selected_creative.campaign.budget / (config.rounds_left + 1)

    price = config.impression_revenue + decimal.Decimal(str(click_probability)) * config.click_revenue \
            + decimal.Decimal(str(conversion_probability)) * config.conversion_revenue

    # Adjust the price based on the remaining budget and rounds left
    adjusted_price = min(price, budget_adjustment)

    return adjusted_price, selected_creative
