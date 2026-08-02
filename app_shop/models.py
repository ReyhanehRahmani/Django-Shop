from django.db import models
from django.contrib.auth.models import User


class SpecialOffer(models.Model):
    image = models.ImageField()
    link = models.URLField()
    location = models.CharField()
    datetime = models.DateTimeField()

    def __str__(self):
        return str(self.datetime)


class Product(models.Model):
    title = models.CharField(null=True, max_length=120)
    sub_title = models.CharField(null=True, max_length=120)

    def __str__(self):
        return self.title


class ProductColor(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(null=True, max_length=20)
    color_code = models.CharField(null=True, max_length=7)
    price = models.IntegerField(null=True)
    price_with_discount = models.IntegerField(null=True)

    def __str__(self):
        return f'{self.product.title} {self.name}'
    
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')
    is_main = models.BooleanField(default=False)

    def __str__(self):
        return f"Image for {self.product.title}"
    
class ProductFeature(models.Model):
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE, 
        related_name='features'
    )
    key = models.CharField(max_length=50)
    value = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.key}: {self.value}"



