from django.contrib.auth.models import User

from rest_framework import serializers

from ..dsp.models.game_config_model import ConfigModel
from ..dsp.models.categories_model import CategoryModel, SubcategoryModel
from ..dsp.models.creative_model import CreativeModel
from ..dsp.models.campaign_model import CampaignModel


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

        # Set the 'config' field to the current game configuration
        validated_data['config'] = current_config

        # Create the campaign object
        campaign = CampaignModel.objects.create(**validated_data)
        return campaign


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
        serialized_subcategories = []
        for category in categories:
            serialized_subcategories.append({'id': category.id, 'code': category.code})
        return serialized_subcategories


