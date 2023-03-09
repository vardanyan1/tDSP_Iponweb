from django.contrib import admin

from .models.game_config_model import ConfigModel
from .models.categories_model import CategoryModel, SubcategoryModel
from .models.campaign_model import CampaignModel
from .models.creative_model import CreativeModel


@admin.register(ConfigModel)
class ConfigModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'current', 'impressions_total', 'auction_type', 'mode', 'budget', 'impression_revenue',
                    'click_revenue', 'conversion_revenue', 'frequency_capping', 'created_at')
    list_filter = ('auction_type', 'mode')
    search_fields = ('id', 'impressions_total', 'budget')


class SubcategoryInline(admin.StackedInline):
    model = SubcategoryModel
    extra = 1


@admin.register(CategoryModel)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ('code', 'tier', 'category')
    search_fields = ('code', 'category')
    inlines = [SubcategoryInline]


@admin.register(SubcategoryModel)
class SubcategoryModelAdmin(admin.ModelAdmin):
    list_display = ('code', 'tier', 'subcategory', 'category')
    search_fields = ('code', 'subcategory', 'category__category')
    list_filter = ('category',)


@admin.register(CampaignModel)
class CampaignModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'budget', 'config_id')
    search_fields = ('name',)

    def config_id(self, obj):
        return obj.config.id


@admin.register(CreativeModel)
class CreativeAdmin(admin.ModelAdmin):
    list_display = ('id', 'external_id', 'name', 'campaign', 'url', 'category_names')
    search_fields = ('external_id', 'name', 'campaign', 'url')

    def campaign_id(self, obj):
        return obj.campaign.name

    def category_names(self, obj):
        return ', '.join([category.subcategory for category in obj.categories.all()])

    category_names.short_description = 'Categories'

    campaign_id.short_description = 'Campaign'
