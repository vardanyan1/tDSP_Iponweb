import decimal

from rest_framework import serializers

from ..dsp.models.bid_request_model import BidRequestModel
from ..dsp.models.bid_response_model import BidResponseModel
from ..dsp.models.campaign_model import CampaignModel
from ..dsp.models.creative_model import CreativeModel
from ..dsp.models.notification_model import NotificationModel


class NotificationSerializer(serializers.ModelSerializer):
    bid_request = serializers.PrimaryKeyRelatedField(queryset=BidRequestModel.objects.all())
    bid_response = serializers.PrimaryKeyRelatedField(queryset=BidResponseModel.objects.all())
    config = serializers.SerializerMethodField()

    class Meta:
        model = NotificationModel
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

        return NotificationModel.objects.create(**validated_data)
