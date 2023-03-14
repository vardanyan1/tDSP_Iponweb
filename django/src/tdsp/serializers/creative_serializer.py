from rest_framework import serializers

from .campaign_serializer import CampaignCreativeSerializer
from ..dsp.models.creative_model import CreativeModel


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

