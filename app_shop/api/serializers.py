# from app_shop.models import SpecialOffer, Product, ProductColor, ProductFeature , ProductImage , Comment
# from rest_framework import serializers


# # class SpecialOfferSerializer(serializers.ModelSerializer):
# #     image = serializers.SerializerMethodField()

# #     def get_image(self, obj):
# #         return 'http://localhost:8000' + obj.image.url

# #     class Meta:
# #         model = SpecialOffer
# #         # fields = ['id', 'image', 'link', 'location', 'datetime']
# #         # fields = '__all__'
# #         exclude = ('datetime', 'id')


# # class ProductSerializer(serializers.ModelSerializer): 
    
# #     colors = serializers.SerializerMethodField()
# #     comments = CommentSerializer(many=True, read_only=True)
# #     average_rating = serializers.SerializerMethodField()     
    
# #     class Meta:
# #         model = Product
# #         fields = ['id', 'name', 'price', 'description', 'comments', 'average_rating']
    
# #     def get_average_rating(self, obj):
# #         comments = obj.comment_set.all()
# #         if comments.exists():
# #             return round(sum(c.rating for c in comments) / comments.count(), 1)
# #         return None
    
# #     def get_colors(self, obj): 
# #         print("Called") 
# #         qs = obj.productcolor_set.all()
# #         serializer = ProductColorSerializer(qs, many=True) 
# #         return serializer.data 
    
# #     class Meta: 
# #         model = Product 
# #         fields = '__all__'


# # class ProductColorSerializer(serializers.ModelSerializer):
# #     class Meta:
# #         model = ProductColor
# #         exclude = ("product",)


# # class ProductFeatureSerializer(serializers.ModelSerializer):
# #     class Meta:
# #         model = ProductFeature
# #         exclude = ("product",)


# # class ProductRequestBodySerializer(serializers.ModelSerializer):

# #     colors = ProductColorSerializer(many=True)
# #     features = ProductFeatureSerializer(many=True)

# #     class Meta:
# #         model = Product
# #         fields = (
# #             "title",
# #             "sub_title",
# #             "colors",
# #             "features",
# #         )


# # class CommentSerializer(serializers.ModelSerializer):
# #     class Meta:
# #         model = Comment
# #         fields = '__all__'


# class CommentSerializer(serializers.ModelSerializer):
#     username = serializers.CharField(source='user.username', read_only=True)
    
#     class Meta:
#         model = Comment
#         fields = ['id', 'user', 'product', 'text', 'rating', 'created_at', 'updated_at']
#         read_only_fields = ['user', 'created_at', 'updated_at']




# class SpecialOfferSerializer(serializers.ModelSerializer):
#     image = serializers.SerializerMethodField()

#     def get_image(self, obj):
#         return 'http://localhost:8000' + obj.image.url

#     class Meta:
#         model = SpecialOffer
#         exclude = ('datetime', 'id')


# class ProductColorSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ProductColor
#         exclude = ("product",)


# class ProductFeatureSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ProductFeature
#         exclude = ("product",)


# class ProductSerializer(serializers.ModelSerializer): 
    
#     colors = serializers.SerializerMethodField()
#     features = serializers.SerializerMethodField()
#     comments = CommentSerializer(many=True, read_only=True)
#     average_rating = serializers.SerializerMethodField()     
    
#     def get_average_rating(self, obj):
#         comments = obj.comment_set.all()
#         if comments.exists():
#             return round(sum(c.rating for c in comments) / comments.count(), 1)
#         return None
    
#     def get_colors(self, obj): 
#         print("Called") 
#         qs = obj.productcolor_set.all()
#         serializer = ProductColorSerializer(qs, many=True) 
#         return serializer.data 
    
#     def get_features(self, obj):  # ← اضافه شد
#         qs = obj.productfeature_set.all()
#         serializer = ProductFeatureSerializer(qs, many=True)
#         return serializer.data
    
#     class Meta: 
#         model = Product 
#         fields = '__all__'


# class ProductRequestBodySerializer(serializers.ModelSerializer):

#     colors = ProductColorSerializer(many=True)
#     features = ProductFeatureSerializer(many=True)

#     class Meta:
#         model = Product
#         fields = (
#             "title",
#             "sub_title",
#             "colors",
#             "features",
#         )

from app_shop.models import SpecialOffer, Product, ProductColor, ProductFeature , ProductImage , Comment
from rest_framework import serializers


class CommentSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Comment
        fields = ['id', 'user', 'text', 'rating', 'created_at', 'updated_at']
        read_only_fields = ['user', 'created_at', 'updated_at']


class SpecialOfferSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        return 'http://localhost:8000' + obj.image.url

    class Meta:
        model = SpecialOffer
        exclude = ('datetime', 'id')


class ProductColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductColor
        exclude = ("product",)


class ProductFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductFeature
        exclude = ("product",)


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'is_main']


class ProductSerializer(serializers.ModelSerializer): 
    
    colors = serializers.SerializerMethodField()
    features = serializers.SerializerMethodField()
    images = ProductImageSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True, source='comment_set')
    
    def get_average_rating(self, obj):
        comments = obj.comment_set.all()
        if comments.exists():
            return round(sum(c.rating for c in comments) / comments.count(), 1)
        return None
    
    def get_comments_count(self, obj):
        return obj.comment_set.count()
    
    def get_colors(self, obj): 
        qs = obj.productcolor_set.all()
        serializer = ProductColorSerializer(qs, many=True) 
        return serializer.data 
    
    def get_features(self, obj):
        qs = obj.productfeature_set.all()
        serializer = ProductFeatureSerializer(qs, many=True)
        return serializer.data

    class Meta: 
        model = Product 
        fields = [
            'id',
            'title',
            'sub_title',
            'colors',
            'features',
            'images',
            'comments',
            'average_rating',
            'comments_count',
        ]


class ProductRequestBodySerializer(serializers.ModelSerializer):

    colors = ProductColorSerializer(many=True)
    features = ProductFeatureSerializer(many=True)

    class Meta:
        model = Product
        fields = (
            "title",
            "sub_title",
            "colors",
            "features",
        )