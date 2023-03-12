import decimal

from django.contrib.auth.models import User

from rest_framework import serializers

from ..dsp.models.bid_request_model import BidRequestModel
from ..dsp.models.bid_response_model import BidResponseModel
from ..dsp.models.game_config_model import ConfigModel
from ..dsp.models.categories_model import CategoryModel, SubcategoryModel
from ..dsp.models.creative_model import CreativeModel
from ..dsp.models.campaign_model import CampaignModel
from ..dsp.models.notification_model import Notification


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'url', 'username', 'email', 'is_staff']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserCreateSerializer(UserSerializer):
    password = serializers.CharField(write_only=True)
    is_staff = serializers.BooleanField(default=False, write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            is_staff=validated_data['is_staff']
        )
        return user

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'is_staff']


class ConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfigModel
        fields = '__all__'


class ConfigCreateSerializer(ConfigSerializer):
    class Meta:
        model = ConfigModel
        exclude = ('current',)


class SubcategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SubcategoryModel
        fields = '__all__'


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    subcategories = SubcategorySerializer(many=True, read_only=True)

    class Meta:
        model = CategoryModel
        fields = '__all__'


class CampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampaignModel
        fields = ['id', 'name', 'budget']

    def create(self, validated_data):
        # Get the current game configuration
        current_config = ConfigModel.objects.get(current=True)

        # Calculate remaining budget in the current configuration
        remaining_budget = current_config.budget - validated_data['budget']

        # If the remaining budget is less than 0, return a BidRequestModel
        if remaining_budget < 0:
            raise serializers.ValidationError("Budget is insufficient to create the campaign.")

        # Set the 'config' field to the current game configuration
        validated_data['config'] = current_config

        # Create the campaign object
        campaign = CampaignModel.objects.create(**validated_data)

        # Update the budget in the current configuration
        current_config.budget = remaining_budget
        current_config.save()

        return campaign

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['budget'] = int(float(representation['budget']))
        return representation



class CampaignCreativeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampaignModel
        fields = ('id', 'name')

    def to_representation(self, instance):
        """
        Override the default serializer method to return a regular dictionary
        instead of an OrderedDict.
        """
        ret = super().to_representation(instance)
        return dict(ret)


class CreativeSerializer(serializers.ModelSerializer):
    categories = serializers.SerializerMethodField()
    campaign = CampaignCreativeSerializer()

    class Meta:
        model = CreativeModel
        fields = ('id', 'external_id', 'name', 'categories', 'campaign', 'url')

    def get_categories(self, obj):
        """
        Serialize categories and their corresponding subcategories.
        """
        categories = obj.categories.all()
        subcategories = obj.subcategories.all()

        # Merge categories and subcategories
        all_categories = list(categories) + list(subcategories)

        # Serialize each category and subcategory
        serialized_categories = [{'id': c.id, 'code': c.code} for c in all_categories]

        return serialized_categories


class AdSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=255)
    imp = serializers.DictField(child=serializers.DictField(child=serializers.IntegerField()))
    click = serializers.DictField(child=serializers.FloatField())
    conv = serializers.DictField(child=serializers.FloatField())
    site = serializers.DictField(child=serializers.CharField(max_length=255))
    ssp = serializers.DictField(child=serializers.CharField(max_length=255))
    user = serializers.DictField(child=serializers.CharField(max_length=255))
    bcat = serializers.ListField(child=serializers.CharField(max_length=255))


class BidRequestSerializer(serializers.ModelSerializer):
    blocked_categories = serializers.SerializerMethodField()

    class Meta:
        model = BidRequestModel
        fields = ('id', 'bid_id', 'banner_width', 'banner_height', 'click_probability', 'conversion_probability',
                  'site_domain', 'ssp_id', 'user_id', 'blocked_categories')

    def get_blocked_categories(self, obj):
        """
        Serialize blocked_categories and their corresponding subcategories.
        """
        categories = obj.blocked_categories.all()
        subcategories = obj.blocked_subcategories.all()

        # Merge categories and subcategories
        all_categories = list(categories) + list(subcategories)

        # Serialize each category and subcategory
        serialized_categories = [{'id': c.id, 'code': c.code} for c in all_categories]

        return serialized_categories


class BidResponseSerializer(serializers.ModelSerializer):
    cat = serializers.SerializerMethodField()
    class Meta:
        model = BidResponseModel
        fields = ['external_id', 'price', 'image_url', 'cat', 'bid_request']

    def create(self, validated_data):
        bid_request = validated_data.pop('bid_request')
        return BidResponseModel.objects.create(bid_request=bid_request, **validated_data)

    def get_cat(self, obj):
        """
        Serialize blocked_categories and their corresponding subcategories.
        """
        categories = obj.categories.all()
        subcategories = obj.subcategories.all()

        # Merge categories and subcategories
        all_categories = list(categories) + list(subcategories)

        # Serialize each category and subcategory
        serialized_categories = [{'id': c.id, 'code': c.code} for c in all_categories]

        return serialized_categories


class NotificationSerializer(serializers.ModelSerializer):
    bid_request = serializers.PrimaryKeyRelatedField(queryset=BidRequestModel.objects.all())
    bid_response = serializers.PrimaryKeyRelatedField(queryset=BidResponseModel.objects.all())
    config = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = '__all__'

    def get_config(self, obj):
        config = obj.bid_request.config.filter(current=True).first()
        if config:
            return config.id
        return None

    def to_internal_value(self, data):
        bid_id = data.get('id', None)
        if bid_id:
            data['bid_id'] = bid_id
        return super().to_internal_value(data)

    def create(self, validated_data):
        # Retrieve the CreativeModel instance related to the BidResponseModel
        creative = CreativeModel.objects.get(external_id=validated_data['bid_response'].external_id)

        # Retrieve the CampaignModel instance related to the CreativeModel
        campaign = CampaignModel.objects.get(id=creative.campaign.id)

        # Calculate remaining budget in the current configuration
        remaining_budget = campaign.budget - decimal.Decimal(str(validated_data['price']))

        # Update the budget in the current configuration
        campaign.budget = remaining_budget
        campaign.save()

        return Notification.objects.create(**validated_data)
