from django.contrib import admin
from app_shop.models import SpecialOffer , Product , ProductColor , ProductFeature , ProductImage , Comment

admin.site.register(SpecialOffer)
admin.site.register(Product)
admin.site.register(ProductColor)
admin.site.register(ProductImage)
admin.site.register(ProductFeature)
admin.site.register(Comment)