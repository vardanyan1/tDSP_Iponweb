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
    """
    ConfigModelAdmin is a Django admin model class that defines display,
    filtering, and search options for the ConfigModel.
    """
    list_display = ('id', 'current', 'impressions_total', 'rounds_left', 'auction_type', 'mode', 'budget',
                    'impression_revenue', 'click_revenue', 'conversion_revenue', 'frequency_capping', 'created_at')
    list_filter = ('auction_type', 'mode')
    search_fields = ('id', 'impressions_total', 'budget')


class CategoryInline(admin.TabularInline):
    """
    CategoryInline is a Django admin TabularInline class that allows
    editing of related CategoryModel instances directly from the
    CategoryModelAdmin form.
    """
    model = CategoryModel
    extra = 1
    fk_name = 'parent'
    fields = ('code', 'name')


@admin.register(CategoryModel)
class CategoryModelAdmin(admin.ModelAdmin):
    """
    CategoryModelAdmin is a Django admin model class that defines display,
    search, and inline editing options for the CategoryModel.
    """
    list_display = ('code', 'name', 'parent')
    search_fields = ('code', 'name', 'parent__name')
    inlines = [CategoryInline]


@admin.register(CampaignModel)
class CampaignModelAdmin(admin.ModelAdmin):
    """
    CampaignModelAdmin is a Django admin model class that defines display
    and search options for the CampaignModel.

    Methods:
    config(obj: CampaignModel) -> int:
        Returns the ID of the related ConfigModel instance.
    """
    list_display = ('id', 'name', 'budget', 'is_active', 'config')
    search_fields = ('name',)

    def config(self, obj):
        return obj.config.id

    config.short_description = 'Config'


class CreativeAdminForm(forms.ModelForm):
    """
    CreativeAdminForm is a Django ModelForm class that defines custom
    form fields and a custom save method for the CreativeModel.

    Methods:
    save(commit: bool = True) -> CreativeModel:
        Custom save method that handles image uploading and URL assignment.
    """
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
    """
    CreativeAdmin is a Django admin model class that defines display,
    search options, and custom form for the CreativeModel.

    Methods:
    categories_display(obj: CreativeModel) -> str:
        Returns a comma-separated string of category names.
    campaign(obj: CreativeModel) -> str:
        Returns the name of the related CampaignModel instance.
    """
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
    """
    BidRequestModelAdmin is a Django admin model class that defines display,
    filtering, and search options for the BidRequestModel, as well as custom
    form and save behavior.

    Methods:
    blocked_categories_display(obj: BidRequestModel) -> str:
        Returns a comma-separated string of blocked category names.
    get_form(request, obj=None, **kwargs) -> forms.ModelForm:
        Customizes the form to hide the 'config' field.
    save_related(request, form, formsets, change) -> None:
        Custom save method that handles saving many-to-many relationships,
        setting the current config, and creating a BidResponse instance.
    """
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
    """
    BidResponseModelAdmin is a Django admin model class that defines display,
    search options, and queryset behavior for the BidResponseModel.

    Methods:
    get_queryset(request) -> QuerySet:
        Customizes the queryset to include related bid_request instances.
    bid_request_id(obj: BidResponseModel) -> str:
        Returns the bid_id of the related BidRequestModel instance.
    """
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
    """
    NotificationModelAdmin is a Django admin model class that defines display,
    filtering, and search options for the NotificationModel, as well as custom
    queryset behavior.

    Methods:
    get_queryset(request) -> QuerySet:
        Customizes the queryset to include related bid_request and bid_response instances.
    """
    list_display = ('id', 'bid_id', 'price', 'win', 'click', 'conversion', 'revenue', 'bid_request', 'bid_response')
    search_fields = ('bid_id',)
    list_filter = ('win', 'click', 'conversion')
    raw_id_fields = ('bid_request', 'bid_response')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('bid_request', 'bid_response')
        return queryset
