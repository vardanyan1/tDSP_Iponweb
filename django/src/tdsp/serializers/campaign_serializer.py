from rest_framework import serializers

from ..dsp.models.campaign_model import CampaignModel


class CampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampaignModel
        fields = ['id', 'name', 'budget', 'is_active', 'min_bid']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_config = self.context.get('current_config', None)

    def validate(self, data):
        """
        Validate the campaign data before creating the instance.

        Args:
            data (dict): The input data for the serializer.

        Returns:
            dict: The validated data.

        Raises:
            serializers.ValidationError: If the data is not valid.
        """
        # If the budget is valid
        if data['budget'] < 0:
            raise serializers.ValidationError({"error": "Budget must be non-negative."})

        # Check if the current game configuration exists
        if not self.current_config:
            raise serializers.ValidationError({"error": "No current game configuration found."})

        # Calculate remaining budget in the current configuration
        remaining_budget = self.current_config.budget - data['budget']

        # If the remaining budget is less than 0
        if remaining_budget < 0:
            raise serializers.ValidationError({"error": "Budget is insufficient to create the campaign."})

        return data

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
