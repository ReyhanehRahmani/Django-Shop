from rest_framework import serializers

from app_shop.models import ProductColor
from app_order.models import Cart , Order


class CartItemSerializer(serializers.ModelSerializer):
    product_title = serializers.SerializerMethodField()
    color_name = serializers.SerializerMethodField()
    color_code = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    price_with_discount = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    item_total_price = serializers.SerializerMethodField()
    item_total_price_with_discount = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = [
            "id",
            "product_title",
            "color_name",
            "color_code",
            "price",
            "price_with_discount",
            "quantity",
            "item_total_price",
            "item_total_price_with_discount",
            "image",
        ]

    def _get_color(self, obj):
        return obj.content_object

    def get_product_title(self, obj):
        color = self._get_color(obj)
        return color.product.title if color else None

    def get_color_name(self, obj):
        color = self._get_color(obj)
        return color.name if color else None

    def get_color_code(self, obj):
        color = self._get_color(obj)
        return color.color_code if color else None

    def get_price(self, obj):
        color = self._get_color(obj)
        return color.price if color else None

    def get_price_with_discount(self, obj):
        color = self._get_color(obj)
        return color.price_with_discount if color else None

    def get_item_total_price(self, obj):
        color = self._get_color(obj)
        if not color or color.price is None:
            return 0
        return color.price * obj.quantity

    def get_item_total_price_with_discount(self, obj):
        color = self._get_color(obj)
        if not color:
            return 0
        unit_price = (
            color.price_with_discount
            if color.price_with_discount is not None
            else (color.price or 0)
        )
        return unit_price * obj.quantity

    def get_image(self, obj):
        color = self._get_color(obj)
        if not color:
            return None
        main_image = color.product.images.filter(is_main=True).first()
        request = self.context.get("request")
        if main_image and request:
            return request.build_absolute_uri(main_image.image.url)
        return main_image.image.url if main_image else None


class AddToCartSerializer(serializers.Serializer):
    color_id = serializers.IntegerField()
    quantity = serializers.IntegerField(default=1, min_value=1)

    def validate_color_id(self, value):
        if not ProductColor.objects.filter(id=value).exists():
            raise serializers.ValidationError("رنگ محصول مورد نظر یافت نشد.")
        return value
    
class OrderListSerializer(serializers.ModelSerializer):

    profile_name = serializers.SerializerMethodField()
    address_full = serializers.SerializerMethodField()
    total_amount = serializers.SerializerMethodField()
    items_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Order
        fields = [
            'id',
            'status',
            'payment_status',
            'paid_amount',
            'total_amount',
            'items_count',
            'created_at',
            'paid_at',
            'profile_name',
            'address_full'
        ]
    
    def get_profile_name(self, obj):

        if obj.profile:
            try:
                return f"{obj.profile.name} {obj.profile.last_name}"
            except AttributeError:
                return "کاربر ناشناس"
        return "کاربر ناشناس"
    
    def get_address_full(self, obj):

        if obj.address:
            try:
                return f"{obj.address.city} - {obj.address.address}"
            except AttributeError:
                return "آدرسی ثبت نشده"
        return "آدرسی ثبت نشده"
    
    def get_total_amount(self, obj):
        cart_items = Cart.objects.filter(id=obj.cart.id)
        total = 0
        for item in cart_items:
            price = item.content_object.price if item.content_object else 0
            total += price * item.quantity
        return total
    
    def get_items_count(self, obj):
        return Cart.objects.filter(id=obj.cart.id).count()