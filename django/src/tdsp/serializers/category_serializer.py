from rest_framework import serializers

from ..dsp.models.categories_model import SubcategoryModel, CategoryModel


class SubcategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SubcategoryModel
        fields = '__all__'


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    subcategories = SubcategorySerializer(many=True, read_only=True)

    class Meta:
        model = CategoryModel
        fields = '__all__'
