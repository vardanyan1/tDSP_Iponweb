from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from ..dsp.models.bid_request_model import BidRequestModel
from ..dsp.models.bid_response_model import BidResponseModel
from ..dsp.models.categories_model import CategoryModel, SubcategoryModel
from ..dsp.models.game_config_model import ConfigModel
from ..serializers.serializers import BidRequestSerializer, BidResponseSerializer, AdSerializer
from ..tools.calculator import calculate_bid_price


class BidViewSet(viewsets.ModelViewSet):
    queryset = BidRequestModel.objects.all()
    serializer_class = BidRequestSerializer

    def create(self, request, *args, **kwargs):
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

            # Get unique category codes
            b_category_codes = set(category for category in blocked_categories)

            # Remove underscores from category codes
            b_category_codes = [code.replace('_', '') for code in b_category_codes]

            # Get subcategory and category objects using a single query
            b_subcategories = SubcategoryModel.objects.filter(code__in=[code for code in b_category_codes if "-" in code])
            b_categories = CategoryModel.objects.filter(code__in=[code for code in b_category_codes if "-" not in code])

            # Determine bid price and image based on the bid request data
            price, image_url, creative_categories, creative_subcategories, creative_external_id, config = calculate_bid_price(
                banner_width, banner_height, click_probability,
                conversion_probability, b_categories, b_subcategories, user_id)

            bid_request = BidRequestModel.objects.create(
                bid_id=bid_id, banner_width=banner_width, banner_height=banner_height,
                click_probability=click_probability, conversion_probability=conversion_probability,
                site_domain=site_domain, ssp_id=ssp_id, user_id=user_id, config=config)

            # Add categories to creative
            for b_category in b_categories:
                bid_request.blocked_categories.add(b_category)

            # Add subcategories to creative
            for b_sub_category in b_subcategories:
                bid_request.blocked_subcategories.add(b_sub_category)

            serializer = BidRequestSerializer(bid_request)
            bid_request.save()

            # Create BidResponseModel instance
            if price:
                bid_response = BidResponseModel.objects.create(
                    external_id=creative_external_id, price=price,
                    image_url=image_url, bid_request=bid_request)

                # Add categories to
                for category in creative_categories:
                    bid_response.categories.add(category)

                # Add subcategories to
                for sub_category in creative_subcategories:
                    bid_response.subcategories.add(sub_category)

                serializer = BidResponseSerializer(bid_response)
                bid_response.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response('No-bid', status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

