from rest_framework import viewsets, pagination

from ..dsp.models.categories_model import CategoryModel
from ..serializers.category_serializer import CategorySerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing category instances.

    Attributes:
        serializer_class (CategorySerializer): The serializer class to use for the viewset.
        queryset (QuerySet): The queryset to use for the viewset.
        pagination_class (PageNumberPagination): The pagination class to use for the viewset.
    """
    serializer_class = CategorySerializer
    queryset = CategoryModel.objects.all()
    pagination_class = pagination.PageNumberPagination
    pagination_class.page_size = 10
