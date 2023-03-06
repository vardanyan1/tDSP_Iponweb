from django.contrib import admin

from .models.game_config_model import ConfigModel


@admin.register(ConfigModel)
class ConfigModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'current', 'impressions_total', 'auction_type', 'mode', 'budget', 'impression_revenue',
                    'click_revenue', 'conversion_revenue', 'frequency_capping')
    list_filter = ('auction_type', 'mode')
    search_fields = ('id', 'impressions_total', 'budget')

