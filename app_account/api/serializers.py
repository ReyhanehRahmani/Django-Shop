from rest_framework import serializers
from app_account.models import UserProfile, Address, UserFavorite
from app_shop.models import ProductColor
from app_order.models import Order, Cart


class AddressSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Address
        fields = ['id', 'city', 'address', 'created_at']


class FavoriteProductColorSerializer(serializers.ModelSerializer):
    
    product_title = serializers.CharField(source='product.title')
    product_sub_title = serializers.CharField(source='product.sub_title')
    
    class Meta:
        model = ProductColor
        fields = ['id', 'product_title', 'product_sub_title', 'name', 'color_code', 'price', 'price_with_discount']


class UserFavoriteSerializer(serializers.ModelSerializer):
    
    content_object = FavoriteProductColorSerializer(read_only=True)
    
    class Meta:
        model = UserFavorite
        fields = ['id', 'content_type', 'object_id', 'content_object']


class OrderCartItemSerializer(serializers.ModelSerializer):
    
    product_title = serializers.CharField(source='content_object.product.title', read_only=True)
    color_name = serializers.CharField(source='content_object.name', read_only=True)
    color_code = serializers.CharField(source='content_object.color_code', read_only=True)
    price = serializers.IntegerField(source='content_object.price', read_only=True)
    price_with_discount = serializers.IntegerField(source='content_object.price_with_discount', read_only=True)
    item_total = serializers.SerializerMethodField()
    
    class Meta:
        model = Cart
        fields = ['id', 'product_title', 'color_name', 'color_code', 'price', 'price_with_discount', 'quantity', 'item_total']
    
    def get_item_total(self, obj):
        price = obj.content_object.price if obj.content_object else 0
        return price * obj.quantity


class OrderSerializer(serializers.ModelSerializer):

    cart_items = serializers.SerializerMethodField()
    total_amount = serializers.SerializerMethodField()
    profile_name = serializers.SerializerMethodField()
    address_full = serializers.SerializerMethodField()
    
    class Meta:
        model = Order
        fields = ['id', 'status', 'paid_amount', 'created_at', 'profile_name', 'address_full', 'cart_items', 'total_amount']
    
    def get_cart_items(self, obj):
        cart_items = Cart.objects.filter(id=obj.cart.id)
        return OrderCartItemSerializer(cart_items, many=True).data
    
    def get_total_amount(self, obj):
        cart_items = Cart.objects.filter(id=obj.cart.id)
        total = 0
        for item in cart_items:
            price = item.content_object.price if item.content_object else 0
            total += price * item.quantity
        return total
    
    def get_profile_name(self, obj):
        if obj.profile:
            return f"{obj.profile.name} {obj.profile.last_name}"
        return "کاربر ناشناس"
    
    def get_address_full(self, obj):
        if obj.address:
            return f"{obj.address.city} - {obj.address.address}"
        return "آدرسی ثبت نشده"


class UserProfileDetailSerializer(serializers.ModelSerializer):

    addresses = serializers.SerializerMethodField()
    favorites = serializers.SerializerMethodField()
    orders = serializers.SerializerMethodField()
    
    class Meta:
        model = UserProfile
        fields = [
            'id', 
            'profile_image', 
            'name', 
            'last_name', 
            'full_name', 
            'phone_number', 
            'email', 
            'address', 
            'addresses', 
            'favorites', 
            'orders', 
            'favorites_count', 
            'created_at', 
            'updated_at'
        ]
    
    def get_addresses(self, obj):
        addresses = Address.objects.filter(user=obj.user)
        return AddressSerializer(addresses, many=True).data
    
    def get_favorites(self, obj):
        favorites = UserFavorite.objects.filter(user=obj.user)
        return UserFavoriteSerializer(favorites, many=True).data
    
    def get_orders(self, obj):
        from django.contrib.contenttypes.models import ContentType
        profile_ct = ContentType.objects.get_for_model(obj)
        orders = Order.objects.filter(profile_type=profile_ct, profile_id=obj.id)
        return OrderSerializer(orders, many=True).data


class UserProfileCreateUpdateSerializer(serializers.ModelSerializer):

    
    class Meta:
        model = UserProfile
        fields = [
            'profile_image', 
            'name', 
            'last_name', 
            'phone_number', 
            'email', 
            'address_type', 
            'address_id'
        ]
    
    def validate_phone_number(self, value):
        
        if value and not value.isdigit():
            raise serializers.ValidationError("شماره تلفن باید فقط شامل اعداد باشد.")
        return value



class UserFavoriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserFavorite
        fields = '__all__'


class UserFavoriteRequestBodySerializer(serializers.Serializer):

    object_id = serializers.IntegerField()
    object_type = serializers.CharField()