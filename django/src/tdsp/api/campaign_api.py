from rest_framework import viewsets, status
from rest_framework.response import Response

from ..dsp.models.campaign_model import CampaignModel
from ..dsp.models.game_config_model import ConfigModel

from ..serializers.campaign_serializer import CampaignSerializer


class CampaignViewSet(viewsets.ModelViewSet):
    """
    This class defines a viewset for the CampaignModel. It handles creating and deleting campaign objects.
    """
    queryset = CampaignModel.objects.all()
    serializer_class = CampaignSerializer

    def create(self, request, *args, **kwargs):
        """
        Create a campaign object if there's a budget for new campaign in game_config.budget.

        Args:
            request (Request): The request object containing the campaign data.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: The response object containing the serialized CampaignModel data or an error response if the request is invalid.

        Raises:
            HTTPError: If the request is not valid.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # If the budget is valid
        if serializer.validated_data['budget'] < 0:
            return Response({"error": "Budget must be non-negative."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Check if the current game configuration exists
        current_config = ConfigModel.objects.filter(current=True).first()
        if not current_config:
            return Response({"error": "No current game configuration found."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Calculate remaining budget in the current configuration
        remaining_budget = current_config.budget - serializer.validated_data['budget']

        # If the remaining budget is less than 0
        if remaining_budget < 0:
            return Response({"error": "Budget is insufficient to create the campaign."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Set the 'config' field to the current game configuration
        serializer.validated_data['config'] = current_config

        # Create the campaign object
        campaign_instance = CampaignModel.objects.create(**serializer.validated_data)

        # Update the budget in the current configuration
        ConfigModel.objects.filter(current=True).update(budget=remaining_budget)

        headers = self.get_success_headers(serializer.data)
        # Update the serializer with the created campaign instance
        serializer = self.get_serializer(campaign_instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        """
        Delete a campaign object and returns the budget of the campaign back to configs budget.

        :param request: (Request): The request object containing the campaign data.

        :return Response: The response object containing a success message or an error response if the campaign object or game configuration does not exist.

        :raise HTTPError: If the request is not valid.
        """
        # Retrieve the campaign object to delete
        campaign = self.get_object()

        # Retrieve the current game configuration or return None if not found
        current_config = ConfigModel.objects.filter(current=True).first()

        # Check if the current game configuration exists
        if not current_config:
            return Response({"error": "No current game configuration found."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Add the campaign's budget back to the game configuration's budget
        updated_budget = current_config.budget + campaign.budget

        # Update the budget in the current configuration
        ConfigModel.objects.filter(current=True).update(budget=updated_budget)

        # Delete the campaign object
        campaign.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
