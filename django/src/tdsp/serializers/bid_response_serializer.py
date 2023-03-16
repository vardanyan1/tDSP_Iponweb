from urllib.parse import urlencode

from rest_framework import serializers

from ..dsp.models.bid_response_model import BidResponseModel


class BidResponseSerializer(serializers.ModelSerializer):
    """
    Serializer for the BidResponse model.
    """
    cat = serializers.SerializerMethodField()

    class Meta:
        model = BidResponseModel
        fields = ['external_id', 'price', 'image_url', 'cat', 'bid_request']

    def create(self, validated_data):
        bid_request = validated_data.pop('bid_request')
        return BidResponseModel.objects.create(bid_request=bid_request, **validated_data)

    def get_cat(self, obj):
        """
        Serialize categories.
        """
        categories = obj.categories.all()

        # Serialize each category
        serialized_categories = [c.code for c in categories]

        return serialized_categories

    def to_representation(self, instance):
        """
        Override the default serializer method to return a regular dictionary
        instead of an OrderedDict.
        """
        data = super().to_representation(instance)

        # Add banner width and height as query parameters to image_url
        banner_width = instance.bid_request.banner_width
        banner_height = instance.bid_request.banner_height
        query_params = urlencode({'w': banner_width, 'h': banner_height})
        data['image_url'] = f"{data['image_url']}?{query_params}"

        # Remove the 'bid_request' field from the response
        data.pop('bid_request', None)
        return data
