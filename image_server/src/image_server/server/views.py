from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ImageSerializer


class SaveImageView(APIView):
    def post(self, request, format=None):
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            image = serializer.save()
            return Response({'url': image.url}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
