from rest_framework import serializers

from ..dsp.models.bid_request_model import BidRequestModel


class BidRequestCreateSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=255)
    imp = serializers.DictField(child=serializers.DictField(child=serializers.IntegerField()))
    click = serializers.DictField(child=serializers.FloatField())
    conv = serializers.DictField(child=serializers.FloatField())
    site = serializers.DictField(child=serializers.CharField(max_length=255))
    ssp = serializers.DictField(child=serializers.CharField(max_length=255))
    user = serializers.DictField(child=serializers.CharField(max_length=255))
    bcat = serializers.ListField(child=serializers.CharField(max_length=255))


class BidRequestSerializer(serializers.ModelSerializer):
    blocked_categories = serializers.SerializerMethodField()

    class Meta:
        model = BidRequestModel
        fields = ('id', 'bid_id', 'banner_width', 'banner_height', 'click_probability', 'conversion_probability',
                  'site_domain', 'ssp_id', 'user_id', 'blocked_categories')

    def get_blocked_categories(self, obj):
        """
        Serialize blocked_categories and their corresponding subcategories.
        """
        categories = obj.blocked_categories.all()
        subcategories = obj.blocked_subcategories.all()

        # Merge categories and subcategories
        all_categories = list(categories) + list(subcategories)

        # Serialize each category and subcategory
        serialized_categories = [{'id': c.id, 'code': c.code} for c in all_categories]

        return serialized_categories
