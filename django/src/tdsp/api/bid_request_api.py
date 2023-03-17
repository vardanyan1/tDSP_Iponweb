from rest_framework import viewsets, status
from rest_framework.response import Response

from ..dsp.models.bid_request_model import BidRequestModel
from ..dsp.models.bid_response_model import BidResponseModel
from ..dsp.models.categories_model import CategoryModel
from ..dsp.models.game_config_model import ConfigModel
from ..serializers.bid_request_serializer import BidRequestSerializer, BidRequestCreateSerializer
from ..serializers.bid_response_serializer import BidResponseSerializer
from ..tools.calculator import calculate_bid_price


class BidViewSet(viewsets.ModelViewSet):
    queryset = BidRequestModel.objects.all()
    serializer_class = BidRequestSerializer

    def create(self, request, *args, **kwargs):
        serializer = BidRequestCreateSerializer(data=request.data)
        if serializer.is_valid():
            bid_request_data = serializer.data

            config = ConfigModel.objects.get(current=True)
            if config.rounds_left <= 0:
                return Response({"error": "No rounds left."},
                                status=status.HTTP_400_BAD_REQUEST)

            bid_id = bid_request_data['id']
            if BidRequestModel.objects.filter(bid_id=bid_id).exists():
                return Response({"error": "BidRequest with this bid_id already exists."},
                                status=status.HTTP_400_BAD_REQUEST)

            imp_data = bid_request_data['imp']
            click_prob = bid_request_data['click']['prob']
            conv_prob = bid_request_data['conv']['prob']
            site_domain = bid_request_data['site']['domain']
            ssp_id = bid_request_data['ssp']['id']
            user_id = bid_request_data['user']['id']
            blocked_categories = bid_request_data['bcat']

            b_category_codes = {code.replace('_', '') for code in blocked_categories}
            b_categories = CategoryModel.objects.filter(code__in=b_category_codes)

            bid_request = BidRequestModel.objects.create(
                bid_id=bid_id,
                banner_width=imp_data['banner']['w'],
                banner_height=imp_data['banner']['h'],
                click_probability=click_prob,
                conversion_probability=conv_prob,
                site_domain=site_domain,
                ssp_id=ssp_id,
                user_id=user_id,
                config=config
            )
            bid_request.blocked_categories.set(b_categories)

            price, creative = calculate_bid_price(bid_request)
            config.rounds_left -= 1
            config.save()

            if price:
                bid_response = BidResponseModel.objects.create(
                    external_id=creative.external_id, price=price,
                    image_url=creative.url, bid_request=bid_request)
                bid_response.categories.set(creative.categories.all())

                serializer = BidResponseSerializer(bid_response)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response('No-bid', status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

