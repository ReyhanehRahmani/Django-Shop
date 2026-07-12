from rest_framework.response import Response
from rest_framework.decorators import api_view
from app_account.models import UserFavorite
from app_account.api.serializers import UserFavoriteSerializer
from django.contrib.contenttypes.models import ContentType

@api_view()
def favorite_list(request):
    """
    Favorite list View
    """
    qs = UserFavorite.objects.all()
    serializer = UserFavoriteSerializer(qs, many=True)
    return Response({
        'result': serializer.data
    })

@api_view(['POST'])
def favorite_create(request):
    """
    Favorite list View
    """
    user_id = request.POST.get('user')
    object_id = request.POST.get('object-id')
    content_type = request.POST.get('object-type')
    if content_type == 'product':
        from app_shop.models import Product
        content_object = Product.objects.get(id=object_id)
    UserFavorite.objects.create(
        user_id=user_id,
        content_object=content_object
    )