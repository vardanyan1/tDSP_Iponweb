from rest_framework import serializers
from ..dsp.models.categories_model import CategoryModel


class CategorySerializer(serializers.ModelSerializer):
    parent = serializers.PrimaryKeyRelatedField(queryset=CategoryModel.objects.all(), allow_null=True)
    children = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = CategoryModel
        fields = ['id', 'name', 'code', 'parent', 'children']
