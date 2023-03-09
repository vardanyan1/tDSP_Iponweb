from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from ..dsp.models.bid_request_model import BidRequestModel
from ..dsp.models.bid_response_model import BidResponseModel
from ..dsp.models.game_config_model import ConfigModel
from ..serializers.serializers import BidRequestSerializer, BidResponseSerializer


class BidViewSet(ViewSet):
    queryset = BidRequestModel.objects.all()
    serializer_class = BidRequestSerializer

    def create(self, request):
        serializer = BidRequestSerializer(data=request.data)
        if serializer.is_valid():
            # Retrieve data from serializer
            bid_id = serializer.validated_data.get('bid_id')
            banner_width = serializer.validated_data.get('banner_width')
            banner_height = serializer.validated_data.get('banner_height')
            click_probability = serializer.validated_data.get('click_probability')
            conversion_probability = serializer.validated_data.get('conversion_probability')
            site_domain = serializer.validated_data.get('site_domain')
            ssp_id = serializer.validated_data.get('ssp_id')
            user_id = serializer.validated_data.get('user_id')
            blocked_categories = serializer.validated_data.get('blocked_categories')

            # Determine bid price and image based on the bid request data
            price, image_url, cat = calculate_bid_price(banner_width, banner_height, click_probability,
                                                        conversion_probability, blocked_categories, user_id)

            # Create BidRequestModel instance
            config = ConfigModel.objects.filter(current=True).first()

            bid_request = BidRequestModel.objects.create(
                banner_width=banner_width, banner_height=banner_height, click_probability=click_probability,
                conversion_probability=conversion_probability, site_domain=site_domain, ssp_id=ssp_id,
                user_id=user_id, config=config)

            if blocked_categories:
                bid_request.blocked_categories.set(blocked_categories)

            # Create BidResponseModel instance
            if price:
                bid_response = BidResponseModel.objects.create(
                    external_id=bid_id, price=price, image_url=image_url, bid_request=bid_request)

                if blocked_categories:
                    bid_response.cat.set(blocked_categories)
                serializer = BidResponseSerializer(bid_response)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response('No-bid', status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def calculate_bid_price(banner_width, banner_height, click_probability,
                        conversion_probability, blocked_categories, user_id):
    # TODO: Implement logic to determine bid price based on bid request data
    price = 2.50
    image_url = 'http://localhost:8001/media/Vek8fPqd8mop5UBpaD7TClRg25kcbflB.jpg'
    cat = "category"

    return price, image_url, cat
