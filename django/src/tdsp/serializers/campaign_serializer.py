from rest_framework import serializers

from ..dsp.models.campaign_model import CampaignModel
from ..dsp.models.game_config_model import ConfigModel


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