from rest_framework import viewsets, pagination
from ..serializers.serializers import CategorySerializer, SubcategorySerializer
from ..dsp.models.categories_model import CategoryModel, SubcategoryModel


class CategoryViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing category instances.
    """
    serializer_class = CategorySerializer
    queryset = CategoryModel.objects.all()


class SubcategoryViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing subcategory instances.
    """
    serializer_class = SubcategorySerializer
    queryset = SubcategoryModel.objects.all()
    pagination_class = pagination.PageNumberPagination
    pagination_class.page_size = 10
