from rest_framework import serializers

from ..dsp.models.creative_model import CreativeModel
from ..dsp.models.categories_model import CategoryModel
from ..dsp.models.campaign_model import CampaignModel


class CategoryFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = ('id', 'code')


class CreativeCampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampaignModel
        fields = ('id', 'name')

    def to_internal_value(self, data):
        if isinstance(data, int):
            try:
                campaign = CampaignModel.objects.get(pk=data)
                return campaign
            except CampaignModel.DoesNotExist:
                raise serializers.ValidationError("Campaign with the provided ID does not exist.")
        return super().to_internal_value(data)


class CreativeSerializer(serializers.ModelSerializer):
    categories = CategoryFieldSerializer(many=True, read_only=True)
    campaign = CreativeCampaignSerializer()

    class Meta:
        model = CreativeModel
        fields = ('id', 'external_id', 'name', 'categories', 'campaign', 'url')

    def validate(self, data):
        external_id = data.get('external_id')

        # Check if the external_id already exists
        if CreativeModel.objects.filter(external_id=external_id).exists():
            raise serializers.ValidationError({"error": "Creative with this external_id already exists."})

        return data
