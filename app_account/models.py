from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType


class UserFavorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveBigIntegerField(null=True)
    content_object = GenericForeignKey("content_type", "object_id")

    def __str__(self):
        return f'{self.user} {self.content_type} {self.object_id}'


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    city = models.CharField(max_length=100)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.city}"
    

class UserProfile(models.Model):

    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='profile'
    )
    profile_image = models.ImageField(
        upload_to='profiles/', 
        null=True, 
        blank=True
    )
    name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    
    address_type = models.ForeignKey(
        ContentType, 
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    address_id = models.PositiveBigIntegerField(null=True, blank=True)
    address = GenericForeignKey('address_type', 'address_id')
    
    favorites = GenericRelation(
        UserFavorite,
        content_type_field='content_type',
        object_id_field='object_id'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.name} {self.last_name}"

    @property
    def full_name(self):
        if self.name and self.last_name:
            return f"{self.name} {self.last_name}"
        return self.user.username

    @property
    def favorites_count(self):
        return self.favorites.count()