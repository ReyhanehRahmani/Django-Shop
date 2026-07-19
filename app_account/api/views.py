from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from app_account.models import UserFavorite
from app_account.api.serializers import UserFavoriteSerializer, UserFavoriteRequestBodySerializer
from django.contrib.contenttypes.models import ContentType
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework_simplejwt.authentication import JWTAuthentication

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


@swagger_auto_schema(
    method='post',
    responses={
        201: 'create favorite',
        204: 'delete favorite',
        400: 'invalid number',
        404: 'content type not found',
    },
    request_body=UserFavoriteRequestBodySerializer,
)
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def favorite(request):
    """
    Favorite list View
    """
    serializer = UserFavoriteRequestBodySerializer(data=request.POST)
    user_id = request.user.id
    try:
        if serializer.is_valid():
            object_id = serializer.data['object_id']
            object_type = serializer.data['object_type']
            product_ct = ContentType.objects.get(model=object_type)
        # else:
        #     return somethong
    except ContentType.DoesNotExist:
        data = {
            'message': 'Invalid Content Type!',
            'status': 'not ok'
        }
        return Response(data=data, status=status.HTTP_404_NOT_FOUND)
    user_favorite = None
    fields = {
        'user_id': user_id,
        'object_id': object_id,
        'content_type': product_ct
    }
    user_favorite, created = UserFavorite.objects.get_or_create(**fields)
    if created:
        # create if doe's not exist
        return Response(data={'status': 'ok'}, status=status.HTTP_201_CREATED)
    else:
        # delete if exists
        user_favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)