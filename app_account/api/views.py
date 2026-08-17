from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from app_account.models import UserFavorite , UserProfile , Address
from django.contrib.contenttypes.models import ContentType
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from rest_framework.generics import RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView , ListCreateAPIView , RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
import random
import jwt
from django.conf import settings
from datetime import datetime, timedelta
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from django.utils import timezone
from app_account.models import PhoneOTP, EmailOTP
from app_email.utils import send_simple_email

from app_account.api.serializers import (
    UserFavoriteSerializer, 
    UserFavoriteRequestBodySerializer,
    UserProfileDetailSerializer,
    UserProfileCreateUpdateSerializer,
    AddressSerializer,
    AddressCreateUpdateSerializer,
    EmailSerializer,
    EmailOTPSerializer,
    PhoneNumberSerializer,
    PhoneOTPSerializer,
    UserRegistrationSerializer,
    UserProfileCreateUpdateSerializer,)



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
        

class SendEmailOTPView(APIView):
    """
    ارسال کد تایید به ایمیل (هم برای بار اول و هم ارسال مجدد)
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = EmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        # بررسی OTP قبلی
        try:
            otp_instance = EmailOTP.objects.get(email=email)
            
            if otp_instance.is_verified:
                return Response(
                    {"detail": "این ایمیل قبلاً تایید شده است."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # اگر هنوز منقضی نشده، خطا بده
            if not otp_instance.is_expired():
                remaining = int((otp_instance.created_at + timedelta(minutes=2) - timezone.now()).total_seconds())
                return Response(
                    {
                        "detail": f"کد قبلی هنوز معتبر است. {remaining} ثانیه دیگر تلاش کنید.",
                        "remaining_seconds": remaining
                    },
                    status=status.HTTP_429_TOO_MANY_REQUESTS
                )
            
            # ساخت OTP جدید
            otp_instance = EmailOTP.create_otp(email)
            
        except EmailOTP.DoesNotExist:
            otp_instance = EmailOTP.create_otp(email)

        # ارسال ایمیل
        email_sent = send_simple_email(
            subject="کد تایید ورود",
            message=f"کد تایید شما: {otp_instance.otp_code}\nاین کد تا ۲ دقیقه دیگر معتبر است.",
            recipient_list=[email],
        )

        if not email_sent:
            return Response(
                {"detail": "ارسال ایمیل با خطا مواجه شد."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(
            {"detail": "کد تایید به ایمیل شما ارسال شد.", "email": email},
            status=status.HTTP_200_OK
        )


class SendPhoneOTPView(APIView):
    """
    ارسال کد تایید به شماره تلفن (هم برای بار اول و هم ارسال مجدد)
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PhoneNumberSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data['phone_number']

        # بررسی OTP قبلی
        try:
            otp_instance = PhoneOTP.objects.get(phone_number=phone_number)
            
            if otp_instance.is_verified:
                return Response(
                    {"detail": "این شماره تلفن قبلاً تایید شده است."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # اگر هنوز منقضی نشده، خطا بده
            if not otp_instance.is_expired():
                remaining = int((otp_instance.created_at + timedelta(minutes=2) - timezone.now()).total_seconds())
                return Response(
                    {
                        "detail": f"کد قبلی هنوز معتبر است. {remaining} ثانیه دیگر تلاش کنید.",
                        "remaining_seconds": remaining
                    },
                    status=status.HTTP_429_TOO_MANY_REQUESTS
                )
            
            # ساخت OTP جدید
            otp_instance = PhoneOTP.create_otp(phone_number)
            
        except PhoneOTP.DoesNotExist:
            otp_instance = PhoneOTP.create_otp(phone_number)

        # ===== در محیط واقعی اینجا SMS ارسال کن =====
        # فعلاً در ترمینال چاپ میشه
        print(f"📱 کد OTP برای {phone_number}: {otp_instance.otp_code}")

        return Response(
            {"detail": "کد تایید به شماره تلفن شما ارسال شد.", "phone_number": phone_number},
            status=status.HTTP_200_OK
        )
    
    
class VerifyOTPView(APIView):
    """
    تایید کد OTP و برگرداندن توکن موقت برای مرحله بعد
    """
    permission_classes = [AllowAny]

    def post(self, request):
        otp_code = request.data.get('otp_code')
        phone_number = request.data.get('phone_number')
        email = request.data.get('email')

        if not otp_code:
            return Response(
                {"detail": "کد تایید الزامی است."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not phone_number and not email:
            return Response(
                {"detail": "شماره تلفن یا ایمیل الزامی است."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if phone_number and email:
            return Response(
                {"detail": "فقط یکی از شماره تلفن یا ایمیل را وارد کنید."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # ===== تایید OTP =====
        if phone_number:
            try:
                otp_instance = PhoneOTP.objects.get(phone_number=phone_number)
            except PhoneOTP.DoesNotExist:
                return Response(
                    {"detail": "شماره تلفن یافت نشد."},
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            try:
                otp_instance = EmailOTP.objects.get(email=email)
            except EmailOTP.DoesNotExist:
                return Response(
                    {"detail": "ایمیل یافت نشد."},
                    status=status.HTTP_404_NOT_FOUND
                )

        if otp_instance.is_expired():
            return Response(
                {"detail": "کد تایید منقضی شده است."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if otp_instance.otp_code != otp_code:
            return Response(
                {"detail": "کد تایید اشتباه است."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # ===== علامت‌گذاری به عنوان تایید شده =====
        otp_instance.is_verified = True
        otp_instance.save()

        # ===== ساخت توکن موقت (برای مرحله ثبت‌نام) =====
        verification_token = jwt.encode(
            {
                'phone_number': phone_number,
                'email': email,
                'exp': datetime.utcnow() + timedelta(minutes=5)  # ۵ دقیقه اعتبار
            },
            settings.SECRET_KEY,
            algorithm='HS256'
        )

        return Response({
            "status": "ok",
            "message": "کد تایید شد.",
            "verification_token": verification_token,  # ✅ فقط همینو برگردون
            "phone_number": phone_number,
            "email": email
        }, status=status.HTTP_200_OK)


class UserRegistrationView(APIView):
    """
    ساخت کاربر جدید با توکن تایید
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        verification_token = serializer.validated_data['verification_token']

        # ===== اعتبارسنجی توکن =====
        try:
            payload = jwt.decode(
                verification_token,
                settings.SECRET_KEY,
                algorithms=['HS256']
            )
        except jwt.ExpiredSignatureError:
            return Response(
                {"detail": "توکن منقضی شده است. دوباره کد تایید بگیرید."},
                status=status.HTTP_400_BAD_REQUEST
            )
        except jwt.InvalidTokenError:
            return Response(
                {"detail": "توکن نامعتبر است."},
                status=status.HTTP_400_BAD_REQUEST
            )

        phone_number = payload.get('phone_number')
        email = payload.get('email')

        # ===== بررسی اینکه OTP تایید شده باشه =====
        if phone_number:
            try:
                otp_instance = PhoneOTP.objects.get(phone_number=phone_number)
                if not otp_instance.is_verified:
                    return Response(
                        {"detail": "کد تایید نشده است."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            except PhoneOTP.DoesNotExist:
                return Response(
                    {"detail": "شماره تلفن یافت نشد."},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # ساخت کاربر (بدون ایمیل)
            user = User.objects.create_user(
                username=username,
                password=password
            )
            
        else:  # email
            try:
                otp_instance = EmailOTP.objects.get(email=email)
                if not otp_instance.is_verified:
                    return Response(
                        {"detail": "کد تایید نشده است."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            except EmailOTP.DoesNotExist:
                return Response(
                    {"detail": "ایمیل یافت نشد."},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # ساخت کاربر با ایمیل
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email
            )

        # ===== ساخت توکن JWT نهایی =====
        refresh = RefreshToken.for_user(user)

        return Response({
            "status": "ok",
            "message": "کاربر با موفقیت ساخته شد.",
            "user_id": user.id,
            "username": user.username,
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        }, status=status.HTTP_200_OK)