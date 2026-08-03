import random
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.utils import timezone

from app_shop.models import (
    Product,
    ProductColor,
    ProductImage,
    ProductFeature,
    SpecialOffer,
)


class Command(BaseCommand):
    help = "Generate fake shop data"

    def handle(self, *args, **kwargs):

        # پاک کردن اطلاعات قبلی
        ProductImage.objects.all().delete()
        ProductColor.objects.all().delete()
        ProductFeature.objects.all().delete()
        Product.objects.all().delete()
        SpecialOffer.objects.all().delete()

        colors = [
            ("مشکی", "#000000"),
            ("سفید", "#FFFFFF"),
            ("قرمز", "#FF0000"),
            ("آبی", "#0000FF"),
            ("سبز", "#00AA00"),
            ("زرد", "#FFFF00"),
            ("نقره‌ای", "#C0C0C0"),
        ]

        feature_keys = {
            "وزن": [
                "150 گرم",
                "200 گرم",
                "250 گرم",
                "300 گرم",
            ],
            "جنس": [
                "پلاستیک",
                "فلز",
                "چرم",
                "پارچه",
            ],
            "کشور سازنده": [
                "ایران",
                "چین",
                "ترکیه",
                "آلمان",
            ],
            "گارانتی": [
                "6 ماه",
                "12 ماه",
                "18 ماه",
                "24 ماه",
            ],
        }

        self.stdout.write("Creating products...")

        for i in range(1, 51):

            product = Product.objects.create(
                title=f"محصول شماره {i}",
                sub_title=f"توضیح کوتاه برای محصول {i}"
            )

            # رنگ‌ها
            for name, code in random.sample(colors, random.randint(2, 5)):
                price = random.randint(100000, 5000000)

                ProductColor.objects.create(
                    product=product,
                    name=name,
                    color_code=code,
                    price=price,
                    price_with_discount=max(
                        price - random.randint(5000, 100000),
                        0
                    ),
                )

            # ویژگی‌ها
            for key, values in feature_keys.items():
                ProductFeature.objects.create(
                    product=product,
                    key=key,
                    value=random.choice(values)
                )

            # تصاویر (برای تست)
            for j in range(random.randint(1, 4)):
                image = ProductImage(
                    product=product,
                    is_main=(j == 0)
                )

                image.image.save(
                    f"product_{i}_{j}.jpg",
                    ContentFile(b"fake image"),
                    save=True
                )

        self.stdout.write("Creating special offers...")

        for i in range(10):

            offer = SpecialOffer(
                link=f"https://example.com/product/{i}",
                location=random.choice([
                    "HOME_TOP",
                    "HOME_MIDDLE",
                    "HOME_BOTTOM",
                ]),
                datetime=timezone.now(),   # این قبلاً جا افتاده بود
            )

            offer.image.save(
                f"offer_{i}.jpg",
                ContentFile(b"fake image"),
                save=False
            )

            offer.save()

        self.stdout.write(
            self.style.SUCCESS("Successfully generated test data.")
        )