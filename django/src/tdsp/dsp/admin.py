from django.contrib import admin
from django import forms

from .models.bid_request_model import BidRequestModel
from .models.bid_response_model import BidResponseModel
from .models.game_config_model import ConfigModel
from .models.categories_model import CategoryModel
from .models.campaign_model import CampaignModel
from .models.creative_model import CreativeModel
from .models.notification_model import NotificationModel
from ..tools.calculator import calculate_bid_price
from ..tools.image_server_tools import send_image


@admin.register(ConfigModel)
class ConfigModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'current', 'impressions_total', 'rounds_left', 'auction_type', 'mode', 'budget',
                    'impression_revenue', 'click_revenue', 'conversion_revenue', 'frequency_capping', 'created_at')
    list_filter = ('auction_type', 'mode')
    search_fields = ('id', 'impressions_total', 'budget')


class CategoryInline(admin.TabularInline):
    model = CategoryModel
    extra = 1
    fk_name = 'parent'
    fields = ('code', 'name')


@admin.register(CategoryModel)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'parent')
    search_fields = ('code', 'name', 'parent__name')
    inlines = [CategoryInline]


@admin.register(CampaignModel)
class CampaignModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'budget', 'is_active', 'config')
    search_fields = ('name',)

    def config(self, obj):
        return obj.config.id

    config.short_description = 'Config'


class CreativeAdminForm(forms.ModelForm):
    file = forms.CharField(label='File', widget=forms.Textarea)

    class Meta:
        model = CreativeModel
        fields = ('external_id', 'name', 'campaign', 'file', 'categories')

    def save(self, commit=True):
        instance = super().save(commit=False)
        encoded_image = self.cleaned_data.get('file')

        # Call the function to send the encoded file to the server and get the URL
        url = send_image(encoded_image)

        # Set the URL of the uploaded file to the instance URL field
        instance.url = url

        if commit:
            instance.save()
            self.save_m2m()

        return instance


@admin.register(CreativeModel)
class CreativeAdmin(admin.ModelAdmin):
    list_display = ('id', 'external_id', 'name', 'campaign', 'url', 'categories_display')
    search_fields = ('external_id', 'name', 'campaign__name', 'url')
    form = CreativeAdminForm

    def categories_display(self, obj):
        return ", ".join([str(category) for category in obj.categories.all()])

    categories_display.short_description = 'Categories'

    def campaign(self, obj):
        return obj.campaign.name

    campaign.short_description = 'Campaign'


@admin.register(BidRequestModel)
class BidRequestModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'bid_id', 'banner_width', 'banner_height', 'click_probability', 'conversion_probability',
                    'site_domain', 'ssp_id', 'user_id', 'config', 'blocked_categories_display')
    search_fields = ('id', 'site_domain', 'ssp_id', 'user_id')
    filter_horizontal = ('blocked_categories',)

    def blocked_categories_display(self, obj):
        return ", ".join([str(category) for category in obj.blocked_categories.all()])

    blocked_categories_display.short_description = 'Blocked Categories'

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        # Exclude the config field from the form
        form.base_fields['config'].widget = forms.HiddenInput()
        form.base_fields['config'].required = False

        return form

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)

        # Save the many-to-many relationships
        obj = form.instance
        obj.blocked_categories.set(form.cleaned_data['blocked_categories'])

        # Set the current config
        obj.config = ConfigModel.objects.filter(current=True).first()

        obj.save()

        # Automatically create a BidResponse if the BidRequest is new and not being updated
        if not change:
            price, creative = calculate_bid_price(obj)

            if price:
                bid_response = BidResponseModel.objects.create(
                    external_id=creative.external_id, price=price, image_url=creative.image_url, bid_request=obj)
                bid_response.save()


@admin.register(BidResponseModel)
class BidResponseModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'external_id', 'price', 'image_url', 'bid_request')
    search_fields = ('external_id', 'bid_request__bid_id')
    raw_id_fields = ('bid_request',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('bid_request')
        return queryset

    def bid_request_id(self, obj):
        return obj.bid_request.bid_id

    bid_request_id.admin_order_field = 'bid_request__bid_id'
    bid_request_id.short_description = 'Bid Request ID'


@admin.register(NotificationModel)
class NotificationModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'bid_id', 'price', 'win', 'click', 'conversion', 'revenue', 'bid_request', 'bid_response')
    search_fields = ('bid_id',)
    list_filter = ('win', 'click', 'conversion')
    raw_id_fields = ('bid_request', 'bid_response')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('bid_request', 'bid_response')
        return queryset
