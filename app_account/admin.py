from django.contrib import admin
from app_account.models import UserFavorite , Address , UserProfile

admin.site.register(UserFavorite)
admin.site.register(Address)
admin.site.register(UserProfile)