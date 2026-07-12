from django.db import models

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