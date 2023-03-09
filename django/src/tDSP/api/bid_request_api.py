from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from ..dsp.models.bid_request_model import BidRequestModel
from ..dsp.models.bid_response_model import BidResponseModel
from ..dsp.models.categories_model import CategoryModel, SubcategoryModel
from ..dsp.models.game_config_model import ConfigModel
from ..serializers.serializers import BidRequestSerializer, BidResponseSerializer, AdSerializer


class BidViewSet(ViewSet):
    queryset = BidRequestModel.objects.all()
    serializer_class = BidRequestSerializer

    def create(self, request):
        serializer = AdSerializer(data=request.data)
        if serializer.is_valid():
            # Retrieve data from serializer
            bid_request_data = serializer.data

            bid_id = bid_request_data['id']
            banner_width = bid_request_data['imp']['banner']['w']
            banner_height = bid_request_data['imp']['banner']['h']
            click_probability = bid_request_data['click']['prob']
            conversion_probability = bid_request_data['conv']['prob']
            site_domain = bid_request_data['site']['domain']
            ssp_id = bid_request_data['ssp']['id']
            user_id = bid_request_data['user']['id']
            blocked_categories = bid_request_data['bcat']

            # Determine bid price and image based on the bid request data
            price, image_url, cat = calculate_bid_price(banner_width, banner_height, click_probability,
                                                        conversion_probability, blocked_categories, user_id)

            # Create BidRequestModel instance
            config = ConfigModel.objects.filter(current=True).first()

            bid_request = BidRequestModel.objects.create(
                bid_id=bid_id, banner_width=banner_width, banner_height=banner_height,
                click_probability=click_probability, conversion_probability=conversion_probability,
                site_domain=site_domain, ssp_id=ssp_id, user_id=user_id, config=config)

            if blocked_categories:
                sub_category_objs = []
                for code in blocked_categories:
                    if '-' in code:
                        sub_category_obj = SubcategoryModel.objects.get(code=code)
                        sub_category_objs.append(sub_category_obj)
                    else:
                        category = CategoryModel.objects.get(code=code)
                        sub_categories = SubcategoryModel.objects.filter(category=category)
                        for sub_category in sub_categories:
                            sub_category_objs.append(sub_category)

                bid_request.blocked_categories.set(sub_category_objs)

            # Create BidResponseModel instance
            if price:
                bid_response = BidResponseModel.objects.create(
                    external_id=bid_id, price=price, image_url=image_url, bid_request=bid_request)

                serializer = BidResponseSerializer(bid_response)
                bid_response.save()
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
