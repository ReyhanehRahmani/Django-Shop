===================================================
Django Shop Project
===================================================

پروژه فروشگاه اینترنتی با استفاده از Django REST Framework

---------------------------------------------------
تکنولوژی‌های استفاده شده
---------------------------------------------------
- Python 3.12
- Django 6.0
- Django REST Framework
- JWT Authentication (SimpleJWT)
- Swagger/OpenAPI (drf-yasg)
- SQLite (توسعه)

---------------------------------------------------
نقش‌های کاربری
---------------------------------------------------
1. مشتری:
   - ثبت‌نام با شماره تلفن + تایید کد OTP
   - مشاهده محصولات
   - افزودن/حذف به سبد خرید
   - ثبت سفارش
   - افزودن/حذف به علاقه‌مندی‌ها
   - کامنت‌گذاری و امتیازدهی

2. ادمین:
   - مدیریت محصولات (ایجاد/ویرایش/حذف)
   - مدیریت ویژگی‌ها و رنگ‌های محصول

---------------------------------------------------
نحوه نصب و اجرا
---------------------------------------------------
1. کلون کردن پروژه:
   git clone https://github.com/ReyhanehRahmani/Django-Shop.git

2. ساخت محیط مجازی:
   python -m venv env
   source env/bin/activate  # Linux/Mac
   env\Scripts\activate     # Windows

3. نصب وابستگی‌ها:
   pip install -r requirements.txt

4. اعمال مایگریشن‌ها:
   python manage.py makemigrations
   python manage.py migrate

5. ساخت کاربر ادمین:
   python manage.py createsuperuser

6. اجرای سرور:
   python manage.py runserver

7. دسترسی به مستندات API:
   http://localhost:8000/swagger/

---------------------------------------------------
APIهای اصلی
---------------------------------------------------
1. احراز هویت:
   POST /api/token/           → دریافت توکن
   POST /api/token/refresh/   → تمدید توکن

2. ثبت‌نام:
   POST /api/account/send-otp/     → ارسال کد
   POST /api/account/verify-otp/   → تایید کد + ساخت کاربر

3. پروفایل:
   GET    /api/account/profile/         → مشاهده پروفایل
   POST   /api/account/profile/create/  → ساخت پروفایل
   PUT    /api/account/profile/update/  → ویرایش پروفایل
   DELETE /api/account/profile/delete/  → حذف پروفایل

4. آدرس‌ها:
   GET    /api/account/addresses/        → لیست آدرس‌ها
   POST   /api/account/addresses/        → ایجاد آدرس جدید
   GET    /api/account/addresses/<id>/   → جزئیات آدرس
   PUT    /api/account/addresses/<id>/   → ویرایش آدرس
   DELETE /api/account/addresses/<id>/   → حذف آدرس

5. سبد خرید:
   GET    /api/order/cart-detail/        → مشاهده سبد
   POST   /api/order/add-to-cart/        → افزودن به سبد
   DELETE /api/order/remove-from-cart/   → حذف از سبد

6. سفارشات:
   GET    /api/order/orders/        → لیست سفارشات
   GET    /api/order/orders/<id>/   → جزئیات سفارش
   POST   /api/order/order/create/  → ثبت سفارش جدید

7. محصولات:
   GET    /api/shop/products/              → لیست محصولات
   GET    /api/shop/product/<id>/          → جزئیات محصول
   POST   /api/shop/product-create/        → ایجاد محصول (ادمین)
   PUT    /api/shop/product-update/<id>/   → ویرایش محصول (ادمین)
   DELETE /api/shop/product-delete/<id>/   → حذف محصول (ادمین)

8. کامنت‌ها:
   GET    /api/shop/product-comment-list/<id>/   → لیست کامنت‌ها
   POST   /api/shop/product/<id>/comment-create/  → ایجاد کامنت
   PUT    /api/shop/comment/<id>/                 → ویرایش کامنت
   DELETE /api/shop/comment/<id>/                 → حذف کامنت

9. علاقه‌مندی‌ها:
   POST /api/account/favorite/        → افزودن/حذف علاقه‌مندی
   GET  /api/account/favorite-list/   → لیست علاقه‌مندی‌ها

---------------------------------------------------
ساختار دیتابیس
---------------------------------------------------
- User (Django default)
- UserProfile (تکمیل اطلاعات کاربر)
- Address (آدرس‌های کاربر)
- Product (محصولات)
- ProductColor (رنگ‌های محصول)
- ProductImage (تصاویر محصول)
- ProductFeature (ویژگی‌های محصول)
- Cart (سبد خرید)
- Order (سفارشات)
- Comment (کامنت‌ها)
- UserFavorite (علاقه‌مندی‌ها)
- PhoneOTP (کدهای تایید)

---------------------------------------------------
نکات امنیتی
---------------------------------------------------
- استفاده از JWT برای احراز هویت
- تفکیک دسترسی ادمین و کاربر عادی
- تایید شماره تلفن با کد OTP
- اعتبارسنجی ورودی‌ها در سریالایزرها

---------------------------------------------------
توسعه‌دهنده
---------------------------------------------------
Reyhaneh Rahmani
GitHub: ReyhanehRahmani

---------------------------------------------------
تاریخ
---------------------------------------------------
مرداد ۱۴۰۵
---------------------------------------------------
ریحانه رحمانی
===================================================