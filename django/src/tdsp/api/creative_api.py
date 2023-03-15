from rest_framework import viewsets, status
from rest_framework.response import Response

from ..dsp.models.creative_model import CreativeModel
from ..dsp.models.categories_model import CategoryModel, SubcategoryModel

from ..serializers.creative_serializer import CreativeSerializer

from ..tools.image_server_tools import send_image


class CreativeViewSet(viewsets.ModelViewSet):
    queryset = CreativeModel.objects.all()
    serializer_class = CreativeSerializer

    def create(self, request, *args, **kwargs):
        # Get data from request
        external_id = request.data.get('external_id')
        name = request.data.get('name')
        campaign_id = request.data.get('campaign')['id']
        encoded_image = request.data.get('file')
        categories = request.data.get('categories')

        # Save image to separate service and get url
        image_url = send_image(encoded_image)

        # Create creative
        creative = CreativeModel.objects.create(external_id=external_id, name=name,
                                                campaign_id=campaign_id, url=image_url)

# TODO: optimize to use a single db query
        # Get unique category codes
        category_codes = set(category['code'] for category in categories)

        # Remove underscores from category codes
        category_codes = [code.replace('_', '') for code in category_codes]

        # Get subcategory and category objects using a single query
        subcategories = SubcategoryModel.objects.filter(code__in=[code for code in category_codes if "-" in code])
        categories = CategoryModel.objects.filter(code__in=[code for code in category_codes if "-" not in code])

        # Add categories to creative
        for category in categories:
            creative.categories.add(category)

        # Add subcategories to creative
        for sub_category in subcategories:
            creative.subcategories.add(sub_category)

        serializer = self.get_serializer(creative)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

