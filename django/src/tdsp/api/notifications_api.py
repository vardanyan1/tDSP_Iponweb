from rest_framework import viewsets
from rest_framework.response import Response

from ..dsp.models.bid_request_model import BidRequestModel
from ..dsp.models.notification_model import NotificationModel

from ..serializers.notif_serializer import NotificationSerializer


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = NotificationModel.objects.all()
    serializer_class = NotificationSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        bid_id = data['id']
        bid_request = BidRequestModel.objects.get(bid_id=bid_id)
        bid_response = bid_request.bidresponsemodel_set.first()
        data['bid_request'] = bid_request.id
        data['bid_response'] = bid_response.id

        serializer = NotificationSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response('', status=200, content_type='text')
        else:
            return Response(serializer.errors, status=400)
