from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics, mixins, permissions , status
from rest_framework.exceptions import PermissionDenied, NotFound
from app_shop.models import SpecialOffer , Product , ProductColor , ProductFeature , Comment , ProductImage
from rest_framework.decorators import api_view
from app_shop.api.serializers import SpecialOfferSerializer ,ProductSerializer , ProductColorSerializer , ProductRequestBodySerializer , CommentSerializer
from rest_framework.generics import ListAPIView 
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from rest_framework.permissions import IsAdminUser
from rest_framework.permissions import AllowAny

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
    qs = Product.objects.prefetch_related(
        'productcolor_set',
        'productfeature_set',
        'comment_set',
        'images'
    ).get(id=product_id)
    
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
@authentication_classes([JWTAuthentication])
@permission_classes([IsAdminUser])
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
            "message": "Product created successfully.",
            "id": product.id 
        },
        status=status.HTTP_201_CREATED
    )


@api_view(["DELETE"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAdminUser])
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
@authentication_classes([JWTAuthentication])
@permission_classes([IsAdminUser])
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


class ProductListView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]
    def get_queryset(self):
        qs = super().get_queryset()
        title = self.request.GET.get('title')
        max_price = self.request.GET.get('max_price')
        min_price = self.request.GET.get('min_price')
        if max_price and min_price:
            qs = qs.filter(productcolor__price__gte=min_price, productcolor__price__lte=max_price)
        return qs.filter(
            Q(title__contains=title) | Q(sub_title__icontains=title)
        ) if title else qs

@api_view()
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def product_comment_list(request, product_id):
    """
    Get all comments for a product
    """
    qs = Comment.objects.filter(product=product_id)
    serializer = CommentSerializer(qs, many=True)
    return Response({
        'result': serializer.data})


class CommentCreateView(generics.CreateAPIView):
    
    serializer_class = CommentSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        product_id = self.kwargs['product_id']
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise NotFound('Product not found.')
        serializer.save(user=self.request.user, product=product)


class CommentUpdateDeleteView(mixins.UpdateModelMixin,mixins.DestroyModelMixin,generics.GenericAPIView):

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = 'comment_id'

    def get_object(self):
        obj = super().get_object()
        if obj.user != self.request.user:
            raise PermissionDenied('You are not allowed to modify this comment.')
        return obj

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
