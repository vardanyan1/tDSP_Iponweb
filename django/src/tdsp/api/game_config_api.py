from rest_framework import viewsets, permissions
from rest_framework.response import Response

from ..dsp.models.campaign_model import CampaignModel
from ..dsp.models.categories_model import CategoryModel
from ..dsp.models.creative_model import CreativeModel
from ..dsp.models.game_config_model import ConfigModel

from ..serializers.config_serializer import ConfigSerializer, ConfigCreateSerializer

from ..tools.image_server_tools import generate_image, send_image


class ConfigViewSet(viewsets.ModelViewSet):
    """
    A viewset for managing game configurations. It provides the ability to create, retrieve,
    update, and delete game configurations.
    """
    queryset = ConfigModel.objects.all()
    serializer_class = ConfigSerializer

    def get_serializer_class(self):
        """
        Return the serializer class to use for the viewset based on the action being performed.

        :return Serializer: The serializer class to use.
        """
        if self.action == 'create':
            return ConfigCreateSerializer
        return ConfigSerializer

    def create(self, request, *args, **kwargs):
        """
       Create a new game configuration object, and if configuration.mode==free, create a free
       campaign with a creative for the configuration.

       :param    request: (Request): The request object containing the data for the new game configuration object.

       :return Response: A response object containing a success message or an error response if the request is invalid.

       :raise HTTPError: If there is an error while creating the game configuration object or the free campaign and creative objects.
       """
        # Delete the old config object, if it exists
        ConfigModel.objects.filter(current=True).delete()

        # Remove the 'current' field from the request data
        data = request.data.copy()
        data.pop('current', None)

        # Set the 'current' field to True
        data['current'] = True

        # Set the rounds_left to number of impressions total
        data['rounds_left'] = data['impressions_total']

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        config = serializer.save()

        if data['mode'] == "free":
            campaign = CampaignModel.objects.create(name='Free Campaign', config=config, budget=data['budget'])

            # Create creative
            image_url = send_image(generate_image(300, 200))
            creative = CreativeModel.objects.create(external_id="free_creative_id", name="Free Creative",
                                                    campaign_id=campaign.id, url=image_url)
            category = CategoryModel.objects.get(code="IAB6-6")
            creative.categories.add(category)

            # Update the budget in the current configuration
            remaining_budget = config.budget - data['budget']
            ConfigModel.objects.filter(current=True).update(budget=remaining_budget)

        headers = self.get_success_headers(serializer.data)
        return Response("", status=200, headers=headers)
