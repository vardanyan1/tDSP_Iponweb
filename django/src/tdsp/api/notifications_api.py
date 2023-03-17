from rest_framework import viewsets, status
from rest_framework.response import Response

from ..dsp.models.bid_request_model import BidRequestModel
from ..dsp.models.creative_model import CreativeModel
from ..dsp.models.notification_model import NotificationModel
from ..dsp.models.user_impression_model import UserImpression

from ..serializers.notif_serializer import NotificationSerializer


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = NotificationModel.objects.all()
    serializer_class = NotificationSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        bid_id = data['id']

        if not BidRequestModel.objects.filter(bid_id=bid_id).exists():
            return Response({"error": "Bid request ID not found."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Check if a notification with the specified bid_id already exists
        if NotificationModel.objects.filter(bid_id=bid_id).exists():
            return Response({"error": "A notification for this bid ID already exists."},
                            status=status.HTTP_400_BAD_REQUEST)

        bid_request = BidRequestModel.objects.get(bid_id=bid_id)
        bid_response = bid_request.bidresponsemodel_set.first()
        data['bid_request'] = bid_request.id
        if bid_response:
            data['bid_response'] = bid_response.id

        serializer = NotificationSerializer(data=data)

        if serializer.is_valid():
            serializer.save()

            # Update UserImpression only if the bid is won
            if data['win']:
                user_id = bid_request.user_id
                creative_external_id = bid_response.external_id
                creative = CreativeModel.objects.get(external_id=creative_external_id)

                user_impression, _ = UserImpression.objects.get_or_create(user_id=user_id, campaign=creative.campaign)
                user_impression.impressions += 1
                user_impression.save()

            return Response('', status=status.HTTP_200_OK, content_type='text/plain')
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
