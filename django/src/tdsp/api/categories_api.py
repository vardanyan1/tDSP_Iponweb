from rest_framework import viewsets, pagination

from ..dsp.models.categories_model import CategoryModel
from ..serializers.category_serializer import CategorySerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing category instances.
    """
    serializer_class = CategorySerializer
    queryset = CategoryModel.objects.all()
    pagination_class = pagination.PageNumberPagination
    pagination_class.page_size = 10
