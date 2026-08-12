from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from app_shop.models import ProductColor
from app_order.models import Cart , Order
from app_order.api.serializers import AddToCartSerializer, CartItemSerializer , OrderListSerializer
from app_account.api.serializers import OrderSerializer
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.exceptions import NotFound
from app_account.models import UserProfile
import random
        

class AddToCartView(generics.CreateAPIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = AddToCartSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        color_id = serializer.validated_data["color_id"]
        quantity = serializer.validated_data["quantity"]

        product_color = ProductColor.objects.select_related("product").get(id=color_id)
        content_type = ContentType.objects.get_for_model(ProductColor)

        cart_item, created = Cart.objects.get_or_create(
            user=request.user,
            content_type=content_type,
            object_id=product_color.id,
            defaults={"quantity": quantity},
        )
        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        output = CartItemSerializer(cart_item, context={"request": request})
        return Response(
            output.data,
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
        )


class RemoveFromCartView(generics.DestroyAPIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CartItemSerializer

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)


class CartDetailView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        content_type = ContentType.objects.get_for_model(ProductColor)
        cart_items = Cart.objects.filter(
            user=request.user,
            content_type=content_type,
        )

        items_data = CartItemSerializer(
            cart_items, many=True, context={"request": request}
        ).data

        total_price = 0
        total_price_with_discount = 0
        for item in cart_items:
            color = item.content_object
            if color is None:
                continue
            unit_price = color.price or 0
            unit_price_with_discount = (
                color.price_with_discount
                if color.price_with_discount is not None
                else unit_price
            )
            total_price += unit_price * item.quantity
            total_price_with_discount += unit_price_with_discount * item.quantity

        return Response(
            {
                "items": items_data,
                "items_count": cart_items.count(),
                "total_quantity": sum(i.quantity for i in cart_items),
                "total_price": total_price,
                "total_price_with_discount": total_price_with_discount,
                "total_discount_amount": total_price - total_price_with_discount,
            }
        )


class OrderListView(ListAPIView):
    """
    لیست سفارشات کاربر جاری
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = OrderListSerializer
    
    def get_queryset(self):
        
        profile_ct = ContentType.objects.get_for_model(UserProfile)
        
        try:
            profile = UserProfile.objects.get(user=self.request.user)
        except UserProfile.DoesNotExist:
            return Order.objects.none()
        
        return Order.objects.filter(
            profile_type=profile_ct,
            profile_id=profile.id
        ).order_by('-created_at')



class OrderDetailView(RetrieveAPIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer
    
    def get_queryset(self):
        
        try:
            profile = UserProfile.objects.get(user=self.request.user)
            profile_ct = ContentType.objects.get_for_model(profile)
            
            return Order.objects.filter(
                profile_type=profile_ct,
                profile_id=profile.id
            ).order_by('-created_at')
            
        except UserProfile.DoesNotExist:
            return Order.objects.none()
    
    def get_object(self):

        index = self.kwargs.get('pk')
        
        try:
            index = int(index)
        except (ValueError, TypeError):
            raise NotFound('شماره سفارش نامعتبر است.')
        
        zero_based_index = index - 1
        
        try:
            return self.get_queryset()[zero_based_index]
        except IndexError:
            raise NotFound(f'سفارش شماره {index} یافت نشد.')
        
class PaymentSimulateView(APIView):
    """
    شبیه‌سازی پرداخت)
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, order_id):

        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response({
                'status': 'not ok',
                'message': 'سفارش یافت نشد.'
            }, status=status.HTTP_404_NOT_FOUND)

        try:
            profile = UserProfile.objects.get(user=request.user)
            profile_ct = ContentType.objects.get_for_model(profile)
            
            if order.profile_type != profile_ct or order.profile_id != profile.id:
                return Response({
                    'status': 'not ok',
                    'message': 'شما به این سفارش دسترسی ندارید.'
                }, status=status.HTTP_403_FORBIDDEN)
        except UserProfile.DoesNotExist:
            return Response({
                'status': 'not ok',
                'message': 'پروفایل یافت نشد.'
            }, status=status.HTTP_404_NOT_FOUND)

        if order.payment_status == 'paid':
            return Response({
                'status': 'not ok',
                'message': 'این سفارش قبلاً پرداخت شده است.'
            }, status=status.HTTP_400_BAD_REQUEST)

        is_successful = random.random() < 0.9

        if is_successful:
            reference = f'PAY-{order.id}-{int(timezone.now().timestamp())}'
            order.mark_as_paid(reference)
            
            return Response({
                'status': 'ok',
                'message': 'پرداخت با موفقیت انجام شد.',
                'data': {
                    'order_id': order.id,
                    'payment_status': order.payment_status,
                    'payment_reference': order.payment_reference,
                    'paid_amount': order.paid_amount,
                    'paid_at': order.paid_at,
                    'order_status': order.status
                }
            }, status=status.HTTP_200_OK)
        else:
            order.payment_status = 'failed'
            order.save()
            
            return Response({
                'status': 'not ok',
                'message': 'پرداخت ناموفق بود. لطفاً مجدداً تلاش کنید.',
                'payment_status': 'failed'
            }, status=status.HTTP_400_BAD_REQUEST)