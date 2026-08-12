from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from app_account.models import UserFavorite , UserProfile , Address , PhoneOTP
from django.contrib.contenttypes.models import ContentType
from rest_framework.generics import RetrieveAPIView
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from app_account.api.serializers import (
    UserFavoriteSerializer, 
    UserFavoriteRequestBodySerializer,
    UserProfileDetailSerializer,
    UserProfileCreateUpdateSerializer,
    AddressSerializer,
    AddressCreateUpdateSerializer,
    PhoneNumberSerializer,
    VerifyOTPSerializer,
    UserProfileCreateUpdateSerializer,
)
from rest_framework.generics import RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView , ListCreateAPIView , RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
import random

@api_view()
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
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
    

class UserProfileDetailView(RetrieveAPIView):
    """
    ویو برای نمایش اطلاعات کامل پروفایل کاربر جاری
    شامل: اطلاعات پایه، آدرس‌ها، علاقه‌مندی‌ها و سفارش‌ها
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileDetailSerializer

    def get_object(self):

        user = self.request.user
        print(f"User: {user.username}, ID: {user.id}")
        
        try:
            return UserProfile.objects.get(user=self.request.user)
        except UserProfile.DoesNotExist:
            raise NotFound('پروفایل کاربر یافت نشد. لطفاً ابتدا پروفایل خود را تکمیل کنید.')


class UserProfileCreateView(CreateAPIView):
    """ایجاد پروفایل برای کاربر جاری"""
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileCreateUpdateSerializer

    def perform_create(self, serializer):
        # بررسی اینکه کاربر قبلاً پروفایل نداشته باشه
        if UserProfile.objects.filter(user=self.request.user).exists():
            from rest_framework.exceptions import ValidationError
            raise ValidationError('کاربر قبلاً پروفایل دارد. برای ویرایش از API update استفاده کنید.')
        
        serializer.save(user=self.request.user)


class UserProfileUpdateView(UpdateAPIView):
    """ویرایش پروفایل کاربر جاری"""
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileCreateUpdateSerializer

    def get_object(self):
        try:
            return UserProfile.objects.get(user=self.request.user)
        except UserProfile.DoesNotExist:
            raise NotFound('پروفایل کاربر یافت نشد. لطفاً ابتدا پروفایل خود را ایجاد کنید.')


class UserProfileDeleteView(DestroyAPIView):
    """حذف پروفایل کاربر جاری"""
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        try:
            return UserProfile.objects.get(user=self.request.user)
        except UserProfile.DoesNotExist:
            raise NotFound('پروفایل کاربر یافت نشد.')

    def destroy(self, request, *args, **kwargs):
        profile = self.get_object()
        profile.delete()
        return Response(
            {'status': 'ok', 'message': 'پروفایل با موفقیت حذف شد.'},
            status=status.HTTP_204_NO_CONTENT
        )


class AddressListView(ListCreateAPIView):
    """
    لیست آدرس‌های کاربر جاری و ایجاد آدرس جدید
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddressCreateUpdateSerializer
        return AddressSerializer
    
    def get_queryset(self):

        return Address.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):

        serializer.save(user=self.request.user)


class AddressDetailView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return AddressCreateUpdateSerializer
        return AddressSerializer
    
    def get_queryset(self):

        return Address.objects.filter(user=self.request.user).order_by('id')
    
    def get_object(self):

        index = self.kwargs.get('pk')
        
        try:

            index = int(index)
        except (ValueError, TypeError):
            raise NotFound('شماره آدرس نامعتبر است.')
        

        zero_based_index = index - 1
        
        try:

            return self.get_queryset()[zero_based_index]
        except IndexError:
            raise NotFound(f'آدرس شماره {index} یافت نشد.')
        

# ======================ثبت نام+=================

@api_view(['POST'])
def send_otp(request):
    serializer = PhoneNumberSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    phone_number = serializer.validated_data['phone_number']
    otp_obj = PhoneOTP.create_otp(phone_number)
    
    print(f"{phone_number}: {otp_obj.otp_code}")
    
    return Response({
        'status': 'ok',
        'message': 'کد تایید با موفقیت ارسال شد.',
        'phone_number': phone_number
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
def resend_otp(request):
    serializer = PhoneNumberSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    phone_number = serializer.validated_data['phone_number']
    
    try:
        otp_obj = PhoneOTP.objects.get(phone_number=phone_number)
        if otp_obj.is_verified:
            return Response({
                'status': 'not ok',
                'message': 'شماره تلفن قبلاً تایید شده است.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        otp_obj = PhoneOTP.create_otp(phone_number)
        print(f"{phone_number}: {otp_obj.otp_code}")
        
        return Response({
            'status': 'ok',
            'message': 'کد جدید با موفقیت ارسال شد.',
            'phone_number': phone_number
        }, status=status.HTTP_200_OK)
        
    except PhoneOTP.DoesNotExist:
        return Response({
            'status': 'not ok',
            'message': 'شماره تلفن یافت نشد. ابتدا درخواست کد کنید.'
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def verify_otp(request):
    """
    تایید کد + ساخت کاربر + برگرداندن توکن
    """
    serializer = VerifyOTPSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    phone_number = serializer.validated_data['phone_number']
    otp_code = serializer.validated_data['otp_code']
    
    try:
        otp_obj = PhoneOTP.objects.get(phone_number=phone_number)
    except PhoneOTP.DoesNotExist:
        return Response({
            'status': 'not ok',
            'message': 'شماره تلفن یافت نشد.'
        }, status=status.HTTP_404_NOT_FOUND)
    
    if otp_obj.is_expired():
        return Response({
            'status': 'not ok',
            'message': 'کد تایید منقضی شده است.'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    if otp_obj.otp_code != otp_code:
        return Response({
            'status': 'not ok',
            'message': 'کد تایید اشتباه است.'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    otp_obj.is_verified = True
    otp_obj.save()
    
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response({
            'status': 'not ok',
            'message': 'نام کاربری و رمز عبور الزامی است.'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    if User.objects.filter(username=username).exists():
        return Response({
            'status': 'not ok',
            'message': 'این نام کاربری قبلاً ثبت شده است.'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    user = User.objects.create_user(
        username=username,
        password=password,
        email=request.data.get('email', '')
    )
    
    refresh = RefreshToken.for_user(user)
    
    return Response({
        'status': 'ok',
        'message': 'شماره تلفن تایید شد و کاربر ساخته شد.',
        'user_id': user.id,
        'username': user.username,
        'access': str(refresh.access_token),
        'refresh': str(refresh)
    }, status=status.HTTP_200_OK)