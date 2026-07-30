from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework_simplejwt.authentication import JWTAuthentication
from app_shop.models import SpecialOffer , Product , ProductColor , ProductFeature
from rest_framework.decorators import api_view
from app_shop.api.serializers import SpecialOfferSerializer ,ProductSerializer , ProductColorSerializer , ProductRequestBodySerializer
    

@api_view()
def special_offer_list(request):

    """
    this is a test
    """
    
    qs = SpecialOffer.objects.last()
    serializer = SpecialOfferSerializer(qs)
    return Response({
        'result': serializer.data})


@api_view()
def product_detail(request, product_id):
    """
    Product Detail View
    """
    qs = Product.objects.get(id=product_id)
    serializer = ProductSerializer(qs)
    return Response({
        'result': serializer.data})


@swagger_auto_schema(
    method='post',
    responses={
        201: 'create favorite',
        204: 'delete favorite',
        400: 'invalid number',
        404: 'content type not found',
    },
    request_body=ProductRequestBodySerializer,)

@api_view(["POST"])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAuthenticated])
def product_create(request):
    """
    Create Product
    """

    serializer = ProductRequestBodySerializer(data=request.data)

    if not serializer.is_valid():
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    validated_data = serializer.validated_data

    colors = validated_data.pop("colors")
    features = validated_data.pop("features")

    if Product.objects.filter(
        title=validated_data["title"],
        sub_title=validated_data["sub_title"]
    ).exists():

        return Response(
            {
                "status": "not ok",
                "message": "Product already exists."
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    product = Product.objects.create(**validated_data)

    # ساخت رنگ‌ها
    for color in colors:
        ProductColor.objects.create(
            product=product,
            **color
        )

    for feature in features:
        ProductFeature.objects.create(
            product=product,
            **feature
        )

    return Response(
        {
            "status": "ok",
            "message": "Product created successfully."
        },
        status=status.HTTP_201_CREATED
    )

@api_view(["DELETE"])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAuthenticated])
def product_delete(request, product_id):
    """
    Delete a product
    """

    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response(
            data={
                "status": "not ok",
                "message": "Product not found."
            },
            status=status.HTTP_404_NOT_FOUND
        )

    product.delete()

    return Response(
        data={
            "status": "ok",
            "message": "Product deleted successfully."
        },
        status=status.HTTP_204_NO_CONTENT
    )

@api_view(["PUT"])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAuthenticated])
def product_update(request, product_id):
    """
    Update Product
    """

    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response(
            {
                "status": "not ok",
                "message": "Product not found."
            },
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = ProductRequestBodySerializer(data=request.data)

    if not serializer.is_valid():
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    validated_data = serializer.validated_data

    colors = validated_data.pop("colors")
    features = validated_data.pop("features")

    product.title = validated_data["title"]
    product.sub_title = validated_data["sub_title"]
    product.save()

    ProductColor.objects.filter(product=product).delete()

    for color in colors:
        ProductColor.objects.create(
            product=product,
            **color
        )

    ProductFeature.objects.filter(product=product).delete()

    for feature in features:
        ProductFeature.objects.create(
            product=product,
            **feature
        )

    return Response(
        {
            "status": "ok",
            "message": "Product updated successfully."
        },
        status=status.HTTP_200_OK
    )
