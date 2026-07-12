from app_account.models import UserFavorite
from rest_framework import serializers


class UserFavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFavorite
        fields = '__all__'
