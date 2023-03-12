import decimal

from django.db.models import Q

from ..dsp.models.creative_model import CreativeModel
from ..dsp.models.game_config_model import ConfigModel


def calculate_bid_price(banner_width, banner_height, click_probability,
                        conversion_probability, b_categories, b_subcategories, user_id):
    # get the current active configuration
    config = ConfigModel.objects.get(current=True)

    # Some logic to choose a price
    price = config.impression_revenue + decimal.Decimal(str(click_probability)) * config.click_revenue \
            + decimal.Decimal(str(conversion_probability)) * config.conversion_revenue

    creatives = CreativeModel.objects.filter(
        Q(campaign__config__current=True) &
        ~Q(categories__in=b_categories) &
        ~Q(subcategories__in=b_subcategories) &
        ~Q(subcategories__category__in=b_categories) &
        Q(campaign__budget__gte=price)
    )

    if creatives:
        # Filter creatives by banner size
        # creatives = creatives.filter(banner_width=banner_width, banner_height=banner_height)

        # Some logic for choosing which one
        creative = creatives[0]

        categories = creative.categories.all()
        subcategories = creative.subcategories.all()
        image_url = creative.url
        creative_external_id = creative.external_id

    else:
        image_url = None
        categories = None
        subcategories = None
        creative_external_id = None
        price = None

    return price, image_url, categories, subcategories, creative_external_id, config
