from django.contrib import admin

from .models.game_config_model import ConfigModel
from .models.categories_model import CategoryModel, SubcategoryModel


@admin.register(ConfigModel)
class ConfigModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'current', 'impressions_total', 'auction_type', 'mode', 'budget', 'impression_revenue',
                    'click_revenue', 'conversion_revenue', 'frequency_capping')
    list_filter = ('auction_type', 'mode')
    search_fields = ('id', 'impressions_total', 'budget')


class SubcategoryInline(admin.StackedInline):
    model = SubcategoryModel
    extra = 1


@admin.register(CategoryModel)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ('IAB_Code', 'Tier', 'IAB_Category')
    search_fields = ('IAB_Code', 'IAB_Category')
    inlines = [SubcategoryInline]


@admin.register(SubcategoryModel)
class SubcategoryModelAdmin(admin.ModelAdmin):
    list_display = ('IAB_Code', 'Tier', 'IAB_Subcategory', 'category')
    search_fields = ('IAB_Code', 'IAB_Subcategory', 'category__IAB_Category')
    list_filter = ('category',)
