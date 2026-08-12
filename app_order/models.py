from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveBigIntegerField(null=True)
    content_object = GenericForeignKey("content_type", "object_id")
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.user} {self.content_type} {self.object_id} x{self.quantity}'


class Order(models.Model):

    STATUS_REGISTERED = 'registered'
    STATUS_PREPARING = 'preparing'
    STATUS_SHIPPED = 'shipped'
    
    STATUS_CHOICES = [
        (STATUS_REGISTERED, 'ثبت شده'),
        (STATUS_PREPARING, 'در حال آماده سازی'),
        (STATUS_SHIPPED, 'ارسال شده'),
    ]

    profile_type = models.ForeignKey(
        ContentType, 
        on_delete=models.CASCADE,
        related_name='order_profiles'  
    )
    profile_id = models.PositiveBigIntegerField()
    profile = GenericForeignKey('profile_type', 'profile_id')

    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)

    paid_amount = models.IntegerField()

    address_type = models.ForeignKey(
        ContentType, 
        on_delete=models.CASCADE,
        related_name='order_addresses' 
    )
    address_id = models.PositiveBigIntegerField()
    address = GenericForeignKey('address_type', 'address_id')

    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default=STATUS_REGISTERED
    )

    payment_status = models.CharField(
    max_length=20,
    choices=[
        ('pending', 'در انتظار پرداخت'),
        ('paid', 'پرداخت شده'),
        ('failed', 'پرداخت ناموفق'),
    ],
    default='pending'
    )

    payment_reference = models.CharField(max_length=100, blank=True, null=True)
    paid_at = models.DateTimeField(null=True, blank=True)


    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"سفارش {self.id}"
    
    def mark_as_paid(self, reference=None):
        self.payment_status = 'paid'
        self.payment_reference = reference or f'PAY-{self.id}-{int(timezone.now().timestamp())}'
        self.paid_at = timezone.now()
        self.status = self.STATUS_PREPARING
        self.save()
