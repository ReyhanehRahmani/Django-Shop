from rest_framework.response import Response
from app_shop.models import SpecialOffer , Product
from rest_framework.decorators import api_view
from app_shop.api.serializers import SpecialOfferSerializer ,ProductSerializer
    

@api_view()
def special_offer_list(request):

    """
    this is a test
    """
    
    qs = SpecialOffer.objects.last()
    serializer = SpecialOfferSerializer(qs)
    return Response({
        'result': serializer.data
    })

@api_view()
def product_detail(request , id):

    """
    details of a product
    """
    
    qs = Product.objects.get(id=id)
    serializer = ProductSerializer(qs)
    return Response({
        'result': serializer.data
    })