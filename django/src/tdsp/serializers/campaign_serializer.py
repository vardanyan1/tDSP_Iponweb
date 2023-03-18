from rest_framework import serializers

from ..dsp.models.campaign_model import CampaignModel


class CampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampaignModel
        fields = ['id', 'name', 'budget', 'is_active']

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
