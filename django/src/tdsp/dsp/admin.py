from django.contrib import admin
from django import forms

from .models.bid_request_model import BidRequestModel
from .models.bid_response_model import BidResponseModel
from .models.game_config_model import ConfigModel
from .models.categories_model import CategoryModel, SubcategoryModel
from .models.campaign_model import CampaignModel
from .models.creative_model import CreativeModel
from ..tools.calculator import calculate_bid_price
from ..tools.image_server_tools import save_image_to_minio


@admin.register(ConfigModel)
class ConfigModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'current', 'impressions_total', 'rounds_left', 'auction_type', 'mode', 'budget',
                    'impression_revenue', 'click_revenue', 'conversion_revenue', 'frequency_capping', 'created_at')
    list_filter = ('auction_type', 'mode')
    search_fields = ('id', 'impressions_total', 'budget')


class SubcategoryInline(admin.StackedInline):
    model = SubcategoryModel
    extra = 1


@admin.register(CategoryModel)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ('code', 'category')
    search_fields = ('code', 'category')
    inlines = [SubcategoryInline]


@admin.register(SubcategoryModel)
class SubcategoryModelAdmin(admin.ModelAdmin):
    list_display = ('code', 'subcategory', 'category')
    search_fields = ('code', 'subcategory', 'category__category')
    list_filter = ('category',)


@admin.register(CampaignModel)
class CampaignModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'budget', 'config_id')
    search_fields = ('name',)

    def config_id(self, obj):
        return obj.config.id


class CreativeAdminForm(forms.ModelForm):
    file = forms.CharField(label='File', widget=forms.Textarea)

    class Meta:
        model = CreativeModel
        fields = ('external_id', 'name', 'campaign', 'file', 'categories')

    def save(self, commit=True):
        instance = super().save(commit=False)
        encoded_image = self.cleaned_data.get('file')

        # Call the function to send the encoded file to the server and get the URL
        url = save_image_to_minio(encoded_image)

        # Set the URL of the uploaded file to the instance URL field
        instance.url = url

        if commit:
            instance.save()

        return instance


@admin.register(CreativeModel)
class CreativeAdmin(admin.ModelAdmin):
    list_display = ('id', 'external_id', 'name', 'campaign', 'url')
    search_fields = ('external_id', 'name', 'campaign', 'url')
    form = CreativeAdminForm

    def campaign_id(self, obj):
        return obj.campaign.name
    #
    # def category_names(self, obj):
    #     return ', '.join([category.subcategory for category in obj.categories.all()])
    #
    # category_names.short_description = 'Categories'
    #
    campaign_id.short_description = 'Campaign'


@admin.register(BidRequestModel)
class BidRequestModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'bid_id', 'banner_width', 'banner_height', 'click_probability', 'conversion_probability',
                    'site_domain', 'ssp_id', 'user_id', 'config')
    list_filter = ('config',)
    search_fields = ('id', 'site_domain', 'ssp_id', 'user_id')
    filter_horizontal = ('blocked_categories',)

    # TODO: write logic for bid response automated generation
    # def save_model(self, request, obj, form, change):
    #     # Determine bid price and image based on the bid request data
    #     price, image_url, cat, creative_external_id = calculate_bid_price(
    #         obj.banner_width, obj.banner_height, obj.click_probability, obj.conversion_probability,
    #         obj.blocked_categories.all(), obj.user_id)
    #
    #     # Set the current config
    #     obj.config = ConfigModel.objects.filter(current=True).first()
    #
    #     # Save the bid request model
    #     obj.save()
    #     obj.blocked_categories.set(form.cleaned_data['blocked_categories'])
    #
    #     # Call the original save_model method to save any other changes
    #     super().save_model(request, obj, form, change)
    #
    #     # Create BidResponseModel instance
    #     if price:
    #         bid_response = BidResponseModel.objects.create(
    #             external_id=creative_external_id, price=price, image_url=image_url, bid_request=obj)
    #
    #         bid_response.save()

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)

        # Save the many-to-many relationships
        obj = form.instance
        obj.blocked_categories.set(form.cleaned_data['blocked_categories'])
        obj.save()

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        # Exclude the config field from the form
        form.base_fields['config'].widget = forms.HiddenInput()
        form.base_fields['config'].required = False

        return form


@admin.register(BidResponseModel)
class BidResponseModelAdmin(admin.ModelAdmin):
    list_display = ('external_id', 'price', 'image_url', 'bid_request')
    list_filter = ('bid_request',)
    search_fields = ('external_id', 'bid_request__bid_id')
