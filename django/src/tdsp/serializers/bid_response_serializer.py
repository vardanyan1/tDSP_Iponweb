from rest_framework import serializers

from ..dsp.models.bid_response_model import BidResponseModel


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

    def to_representation(self, instance):
        """
        Override the default serializer method to return a regular dictionary
        instead of an OrderedDict.
        """
        data = super().to_representation(instance)
        data.pop('bid_request', None)
        return data
