from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from app_account.models import UserProfile, Address, PhoneOTP, UserFavorite
from app_shop.models import Product, ProductColor, ProductFeature, ProductImage, SpecialOffer, Comment
from app_order.models import Cart, Order
import random
from datetime import timedelta
from django.core.files.base import ContentFile
from io import BytesIO
from PIL import Image as PILImage
import os


class Command(BaseCommand):
    help = 'Seed database with 20+ test data for all tables'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🚀 Starting database seeding...'))
        
        # Clear existing data (optional)
        # self.clear_data()
        
        self.create_users()
        self.create_profiles()
        self.create_products()
        self.create_colors()
        self.create_features()
        self.create_images()
        self.create_addresses()
        self.create_carts()
        self.create_orders()
        self.create_comments()
        self.create_favorites()
        self.create_special_offers()
        
        self.stdout.write(self.style.SUCCESS('✅ Database seeding completed!'))

    def clear_data(self):
        self.stdout.write('🗑️ Clearing existing data...')
        Order.objects.all().delete()
        Cart.objects.all().delete()
        Comment.objects.all().delete()
        UserFavorite.objects.all().delete()
        Address.objects.all().delete()
        ProductImage.objects.all().delete()
        ProductColor.objects.all().delete()
        ProductFeature.objects.all().delete()
        Product.objects.all().delete()
        SpecialOffer.objects.all().delete()
        PhoneOTP.objects.all().delete()
        UserProfile.objects.all().delete()
        User.objects.exclude(is_superuser=True).delete()
        self.stdout.write('  ✅ Data cleared!')

    def create_users(self):
        self.stdout.write('📝 Creating 5 users...')
        
        # Create admin
        admin, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@shop.com',
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            admin.set_password('admin123')
            admin.save()
            self.stdout.write(f'  ✅ Admin created: admin/admin123')
        
        # Create 4 regular users
        users_data = [
            {'username': 'reza', 'password': '123456', 'email': 'reza@example.com'},
            {'username': 'dina', 'password': '123456', 'email': 'dina@example.com'},
            {'username': 'kazem', 'password': '123456', 'email': 'kazem@example.com'},
            {'username': 'sara', 'password': '123456', 'email': 'sara@example.com'},
            {'username': 'nadi', 'password': '123456', 'email': 'nadi@example.com'},
        ]
        
        for data in users_data:
            user, created = User.objects.get_or_create(
                username=data['username'],
                defaults={'email': data['email']}
            )
            if created:
                user.set_password(data['password'])
                user.save()
                self.stdout.write(f'  ✅ User created: {data["username"]}')

    def create_profiles(self):
        self.stdout.write('📝 Creating 5 profiles...')
        
        profiles_data = [
            {'user': 'reza', 'name': 'رضا', 'last_name': 'احمدی', 'phone': '09121111111', 'email': 'reza@example.com'},
            {'user': 'dina', 'name': 'دینا', 'last_name': 'رضایی', 'phone': '09122222222', 'email': 'dina@example.com'},
            {'user': 'kazem', 'name': 'کاظم', 'last_name': 'محمدی', 'phone': '09123333333', 'email': 'kazem@example.com'},
            {'user': 'sara', 'name': 'سارا', 'last_name': 'کریمی', 'phone': '09124444444', 'email': 'sara@example.com'},
            {'user': 'nadi', 'name': 'نادی', 'last_name': 'نادری', 'phone': '09125555555', 'email': 'nadi@example.com'},
        ]
        
        for data in profiles_data:
            try:
                user = User.objects.get(username=data['user'])
                profile, created = UserProfile.objects.get_or_create(
                    user=user,
                    defaults={
                        'name': data['name'],
                        'last_name': data['last_name'],
                        'phone_number': data['phone'],
                        'email': data['email']
                    }
                )
                if created:
                    self.stdout.write(f'  ✅ Profile created for {data["user"]}')
            except User.DoesNotExist:
                self.stdout.write(f'  ⚠️ User {data["user"]} not found')

    def create_products(self):
        self.stdout.write('📝 Creating 5 products...')
        
        products_data = [
            {'title': 'کیف چرمی مردانه', 'sub_title': 'مدل کلاسیک مشکی'},
            {'title': 'کفش اسپرت زنانه', 'sub_title': 'راحتی و شیک'},
            {'title': 'لباس مجلسی زنانه', 'sub_title': 'طراحی خاص'},
            {'title': 'عطر مردانه', 'sub_title': 'رایحه گرم و ماندگار'},
            {'title': 'ساعت هوشمند', 'sub_title': 'نسخه جدید پرو'},
            {'title': 'هدفون بی‌سیم', 'sub_title': 'کنسل نویز فعال'},
        ]
        
        for data in products_data:
            product, created = Product.objects.get_or_create(
                title=data['title'],
                defaults={'sub_title': data['sub_title']}
            )
            if created:
                self.stdout.write(f'  ✅ Product created: {data["title"]}')

    def create_colors(self):
        self.stdout.write('📝 Creating 12 colors for products...')
        
        products = Product.objects.all()
        colors_data = [
            {'name': 'مشکی', 'color_code': '#000000', 'price': 350000, 'price_with_discount': 250000},
            {'name': 'قهوه‌ای', 'color_code': '#8B4513', 'price': 380000, 'price_with_discount': 270000},
            {'name': 'سفید', 'color_code': '#FFFFFF', 'price': 450000, 'price_with_discount': 320000},
            {'name': 'صورتی', 'color_code': '#FFB6C1', 'price': 420000, 'price_with_discount': 300000},
            {'name': 'قرمز', 'color_code': '#FF0000', 'price': 550000, 'price_with_discount': 450000},
            {'name': 'طوسی', 'color_code': '#808080', 'price': 200000, 'price_with_discount': 150000},
            {'name': 'آبی', 'color_code': '#0000FF', 'price': 320000, 'price_with_discount': 280000},
            {'name': 'سبز', 'color_code': '#008000', 'price': 280000, 'price_with_discount': 230000},
            {'name': 'زرد', 'color_code': '#FFFF00', 'price': 250000, 'price_with_discount': 200000},
            {'name': 'نارنجی', 'color_code': '#FFA500', 'price': 300000, 'price_with_discount': 260000},
            {'name': 'بنفش', 'color_code': '#800080', 'price': 400000, 'price_with_discount': 350000},
            {'name': 'نقره‌ای', 'color_code': '#C0C0C0', 'price': 220000, 'price_with_discount': 180000},
        ]
        
        for i, product in enumerate(products):
            # Each product gets 2-3 colors
            num_colors = random.randint(2, 3)
            selected_colors = random.sample(colors_data, num_colors)
            
            for color_data in selected_colors:
                ProductColor.objects.create(
                    product=product,
                    name=color_data['name'],
                    color_code=color_data['color_code'],
                    price=color_data['price'],
                    price_with_discount=color_data['price_with_discount']
                )
            
            self.stdout.write(f'  ✅ {num_colors} colors created for {product.title}')

    def create_features(self):
        self.stdout.write('📝 Creating 10 features for products...')
        
        products = Product.objects.all()
        features_data = [
            {'key': 'جنس', 'value': 'چرم طبیعی'},
            {'key': 'جنس', 'value': 'چرم مصنوعی'},
            {'key': 'جنس', 'value': 'پارچه'},
            {'key': 'جنس', 'value': 'ابریشم'},
            {'key': 'جنس', 'value': 'نایلون'},
            {'key': 'اندازه', 'value': '۴۰×۳۰ سانتیمتر'},
            {'key': 'اندازه', 'value': '۵۰×۴۰ سانتیمتر'},
            {'key': 'سایز', 'value': '۳۶-۴۰'},
            {'key': 'سایز', 'value': 'S, M, L'},
            {'key': 'سایز', 'value': 'M, L, XL'},
            {'key': 'حجم', 'value': '۱۰۰ میلی‌لیتر'},
            {'key': 'حجم', 'value': '۵۰ میلی‌لیتر'},
            {'key': 'ماندگاری', 'value': '۲۴ ساعته'},
            {'key': 'ماندگاری', 'value': '۱۲ ساعته'},
        ]
        
        for product in products:
            num_features = random.randint(2, 3)
            selected_features = random.sample(features_data, num_features)
            
            for feature_data in selected_features:
                ProductFeature.objects.create(
                    product=product,
                    key=feature_data['key'],
                    value=feature_data['value']
                )
            
            self.stdout.write(f'  ✅ {num_features} features created for {product.title}')

    def create_images(self):
        self.stdout.write('📝 Creating images for products...')
        
        products = Product.objects.all()
        
        for product in products:
            # Create 2-3 images for each product
            num_images = random.randint(2, 3)
            for i in range(num_images):
                # Create a dummy image
                img = PILImage.new('RGB', (800, 800), color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
                img_io = BytesIO()
                img.save(img_io, 'PNG')
                img_io.seek(0)
                
                image, created = ProductImage.objects.get_or_create(
                    product=product,
                    is_main=(i == 0),
                    defaults={
                        'image': ContentFile(img_io.read(), f'product_{product.id}_image_{i}.png')
                    }
                )
                if created:
                    self.stdout.write(f'  ✅ Image {i+1} created for {product.title}')

    def create_addresses(self):
        self.stdout.write('📝 Creating 8 addresses...')
        
        addresses_data = [
            {'user': 'reza', 'city': 'تهران', 'address': 'خیابان آزادی، پلاک ۱۲۳، واحد ۵'},
            {'user': 'reza', 'city': 'اصفهان', 'address': 'خیابان چهارباغ، پلاک ۴۵'},
            {'user': 'dina', 'city': 'شیراز', 'address': 'خیابان زند، پلاک ۷۸'},
            {'user': 'dina', 'city': 'تهران', 'address': 'خیابان ولیعصر، پلاک ۵۶'},
            {'user': 'kazem', 'city': 'مشهد', 'address': 'خیابان امام رضا، پلاک ۳۲'},
            {'user': 'kazem', 'city': 'تهران', 'address': 'خیابان انقلاب، پلاک ۱۰۰'},
            {'user': 'sara', 'city': 'تبریز', 'address': 'خیابان فردوسی، پلاک ۲۰'},
            {'user': 'nadi', 'city': 'شیراز', 'address': 'خیابان حافظ، پلاک ۶۶'},
        ]
        
        for data in addresses_data:
            try:
                user = User.objects.get(username=data['user'])
                address, created = Address.objects.get_or_create(
                    user=user,
                    city=data['city'],
                    defaults={'address': data['address']}
                )
                if created:
                    self.stdout.write(f'  ✅ Address created for {data["user"]}: {data["city"]}')
            except User.DoesNotExist:
                self.stdout.write(f'  ⚠️ User {data["user"]} not found')

    def create_carts(self):
        self.stdout.write('📝 Creating 10+ cart items...')
        
        users = User.objects.exclude(username='admin')
        products = Product.objects.all()
        
        cart_count = 0
        for user in users:
            # Each user gets 1-3 cart items
            num_items = random.randint(1, 3)
            selected_products = random.sample(list(products), min(num_items, len(products)))
            
            for product in selected_products:
                color = ProductColor.objects.filter(product=product).first()
                if color:
                    content_type = ContentType.objects.get_for_model(ProductColor)
                    
                    cart_item, created = Cart.objects.get_or_create(
                        user=user,
                        content_type=content_type,
                        object_id=color.id,
                        defaults={'quantity': random.randint(1, 3)}
                    )
                    
                    if created:
                        cart_count += 1
                        self.stdout.write(f'  ✅ Cart item for {user.username}: {product.title} x{cart_item.quantity}')
        
        self.stdout.write(f'  📊 Total cart items: {cart_count}')

    def create_orders(self):
        self.stdout.write('📝 Creating 10+ orders...')
        
        users = User.objects.exclude(username='admin')
        order_count = 0
        
        for user in users:
            cart_items = Cart.objects.filter(user=user)
            if not cart_items:
                continue
            
            try:
                profile = UserProfile.objects.get(user=user)
            except UserProfile.DoesNotExist:
                continue
            
            address = Address.objects.filter(user=user).first()
            if not address:
                continue
            
            profile_ct = ContentType.objects.get_for_model(profile)
            address_ct = ContentType.objects.get_for_model(address)
            
            # Create 1-3 orders per user
            num_orders = min(random.randint(1, 3), len(cart_items))
            selected_items = random.sample(list(cart_items), num_orders)
            
            for cart_item in selected_items:
                if Order.objects.filter(cart=cart_item).exists():
                    continue
                
                color = cart_item.content_object
                total = color.price * cart_item.quantity if color else 0
                
                statuses = ['registered', 'preparing', 'shipped']
                
                order = Order.objects.create(
                    profile_type=profile_ct,
                    profile_id=profile.id,
                    cart=cart_item,
                    paid_amount=total,
                    address_type=address_ct,
                    address_id=address.id,
                    status=random.choice(statuses),
                    created_at=timezone.now() - timedelta(days=random.randint(0, 10))
                )
                
                order_count += 1
                self.stdout.write(f'  ✅ Order #{order.id} for {user.username}: {order.status}')
        
        self.stdout.write(f'  📊 Total orders: {order_count}')

    def create_comments(self):
        self.stdout.write('📝 Creating 10+ comments...')
        
        products = Product.objects.all()
        users = User.objects.exclude(username='admin')
        comment_count = 0
        
        comment_texts = [
            'عالی بود، پیشنهاد میکنم!',
            'کیفیت خوبی داشت.',
            'قیمتش مناسب بود.',
            'خیلی راضی بودم.',
            'بهتر از چیزی که فکر میکردم.',
            'دیر رسید ولی ارزشش رو داشت.',
            'کاش رنگ بیشتری داشت.',
            'عالی و باکیفیت',
            'توصیه میکنم به همه',
            'باز هم خرید میکنم',
            'جنس خوبی داشت',
            'اندازه دقیق بود',
            'ارسال سریع بود',
            'بسته‌بندی عالی',
            'قیمت مناسبی داشت',
        ]
        
        for product in products:
            # Each product gets 2-3 comments
            num_comments = random.randint(2, 3)
            selected_users = random.sample(list(users), min(num_comments, len(users)))
            
            for user in selected_users:
                comment, created = Comment.objects.get_or_create(
                    product=product,
                    user=user,
                    defaults={
                        'text': random.choice(comment_texts),
                        'rating': random.randint(1, 5)
                    }
                )
                if created:
                    comment_count += 1
                    self.stdout.write(f'  ✅ Comment for {product.title} by {user.username}')
        
        self.stdout.write(f'  📊 Total comments: {comment_count}')

    def create_favorites(self):
        self.stdout.write('📝 Creating 10+ favorites...')
        
        users = User.objects.exclude(username='admin')
        products = Product.objects.all()
        favorite_count = 0
        
        for user in users:
            # Each user favorites 2-3 products
            num_favorites = random.randint(2, 3)
            selected_products = random.sample(list(products), min(num_favorites, len(products)))
            
            for product in selected_products:
                color = ProductColor.objects.filter(product=product).first()
                if not color:
                    continue
                
                content_type = ContentType.objects.get_for_model(ProductColor)
                
                favorite, created = UserFavorite.objects.get_or_create(
                    user=user,
                    content_type=content_type,
                    object_id=color.id
                )
                if created:
                    favorite_count += 1
                    self.stdout.write(f'  ✅ Favorite for {user.username}: {product.title}')
        
        self.stdout.write(f'  📊 Total favorites: {favorite_count}')

    def create_special_offers(self):
        self.stdout.write('📝 Creating special offers...')
        
        # Skip if no image files available
        self.stdout.write('  ⏭ Skipping special offers (requires image files)')
