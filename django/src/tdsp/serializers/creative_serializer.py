from rest_framework import serializers

from .campaign_serializer import CampaignCreativeSerializer
from ..dsp.models.creative_model import CreativeModel
from ..dsp.models.categories_model import CategoryModel


class CategoryFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = ('id', 'code')


class CreativeSerializer(serializers.ModelSerializer):
    categories = CategoryFieldSerializer(many=True, read_only=True)
    campaign = CampaignCreativeSerializer()

    class Meta:
        model = CreativeModel
        fields = ('id', 'external_id', 'name', 'categories', 'campaign', 'url')
