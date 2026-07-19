from rest_framework import serializers
from app_account.models import UserFavorite


class UserFavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFavorite
        fields = '__all__'


class UserFavoriteRequestBodySerializer(serializers.Serializer):
    object_id = serializers.IntegerField()
    object_type = serializers.CharField()
