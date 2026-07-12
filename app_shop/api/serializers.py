from app_shop.models import SpecialOffer, Product, ProductColor
from rest_framework import serializers


class SpecialOfferSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        return 'http://localhost:8000' + obj.image.url

    class Meta:
        model = SpecialOffer
        # fields = ['id', 'image', 'link', 'location', 'datetime']
        # fields = '__all__'
        exclude = ('datetime', 'id')


class ProductColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductColor
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    colors = serializers.SerializerMethodField()

    def get_colors(self, obj):
        print("Called")
        qs = obj.productcolor_set.all()
        serializer = ProductColorSerializer(qs, many=True)
        return serializer.data
    
    class Meta:
        model = Product
        fields = '__all__'