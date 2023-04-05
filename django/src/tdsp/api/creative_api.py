from rest_framework import viewsets, status
from rest_framework.response import Response

from ..dsp.models.creative_model import CreativeModel
from ..dsp.models.categories_model import CategoryModel

from ..serializers.creative_serializer import CreativeSerializer

from ..tools.image_server_tools import send_image


class CreativeViewSet(viewsets.ModelViewSet):
    queryset = CreativeModel.objects.all()
    serializer_class = CreativeSerializer

    def create(self, request, *args, **kwargs):
        """
        Create a new creative object with the given data, save the image to a separate service, and assign categories to it.

        :param  request: (Request) The request object containing the data for the new creative object.

        :return Response: A response object containing the serialized data of the new creative object or an error response if the request is invalid.

        :raise HTTPError: If there is an error while creating the creative object.
        """
        # Get data from request
        external_id = request.data.get('external_id')
        name = request.data.get('name')
        campaign_id = request.data.get('campaign')['id']
        encoded_image = request.data.get('file')
        categories = request.data.get('categories')

        # Save image to separate service and get url
        image_url = send_image(encoded_image)

        # Create creative using the serializer
        serializer = self.get_serializer(data={
            'external_id': external_id,
            'name': name,
            'campaign': campaign_id,
            'url': image_url,
            'categories': categories
        })
        serializer.is_valid(raise_exception=True)
        creative = serializer.save()

        # Set categories
        creative.categories.set(CategoryModel.objects.filter(
            code__in=[category['code'].replace('_', '') for category in categories])
        )

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
