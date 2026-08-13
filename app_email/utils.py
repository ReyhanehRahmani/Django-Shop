# app_email/utils.py

from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
import logging

# راه‌اندازی لاگر برای ثبت خطاها
logger = logging.getLogger(__name__)


def send_simple_email(subject, message, recipient_list):
    """
    ارسال یک ایمیل ساده (متن ساده)
    
    پارامترها:
    - subject: موضوع ایمیل
    - message: متن ایمیل
    - recipient_list: لیست گیرندگان (مثلاً ['user@email.com'])
    
    برگرداندن:
    - True اگر ایمیل با موفقیت فرستاده شد
    - False اگر خطایی رخ داد
    """
    from_email = settings.DEFAULT_FROM_EMAIL
    
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=recipient_list,
            fail_silently=False,  # اگر خطا بود، استثنا پرتاب کن
        )
        logger.info(f"ایمیل با موفقیت به {recipient_list} فرستاده شد")
        return True
    except Exception as e:
        logger.error(f"خطا در ارسال ایمیل: {str(e)}")
        return False

# app_email/utils.py

from django.core.mail import send_mail
from django.conf import settings


def send_test_email():
    """
    یک ایمیل تست خیلی ساده می‌فرسته
    """
    send_mail(
        subject='سلام دنیا!',
        message='این اولین ایمیل منه!',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=['test@example.com'],
    )


# بقیه توابع قبلی مثل send_html_email و ... بعد از این بیایید

def send_html_email(subject, html_content, recipient_list):
    """
    ارسال ایمیل با قالب HTML
    
    پارامترها:
    - subject: موضوع ایمیل
    - html_content: محتوای HTML ایمیل
    - recipient_list: لیست گیرندگان
    """
    from_email = settings.DEFAULT_FROM_EMAIL
    
    try:
        # تبدیل HTML به متن ساده (برای ایمیل‌هایی که HTML رو پشتیبانی نمی‌کنن)
        text_content = strip_tags(html_content)
        
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=from_email,
            to=recipient_list,
        )
        email.attach_alternative(html_content, "text/html")
        email.send()
        
        logger.info(f"ایمیل HTML با موفقیت به {recipient_list} فرستاده شد")
        return True
    except Exception as e:
        logger.error(f"خطا در ارسال ایمیل HTML: {str(e)}")
        return False


def send_templated_email(subject, template_name, context, recipient_list):
    """
    ارسال ایمیل با استفاده از قالب‌های Django
    
    پارامترها:
    - subject: موضوع ایمیل
    - template_name: نام فایل قالب (مثلاً 'email/welcome.html')
    - context: دیکشنری داده‌های قالب
    - recipient_list: لیست گیرندگان
    """
    from_email = settings.DEFAULT_FROM_EMAIL
    
    try:
        # رندر کردن قالب HTML
        html_content = render_to_string(template_name, context)
        
        # تبدیل به متن ساده
        text_content = strip_tags(html_content)
        
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=from_email,
            to=recipient_list,
        )
        email.attach_alternative(html_content, "text/html")
        email.send()
        
        logger.info(f"ایمیل قالبی با موفقیت به {recipient_list} فرستاده شد")
        return True
    except Exception as e:
        logger.error(f"خطا در ارسال ایمیل قالبی: {str(e)}")
        return False
    

# app_email/utils.py

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


def send_welcome_email(user_email, user_name, activation_link):
    """
    ارسال ایمیل خوش‌آمدگویی با قالب HTML
    
    پارامترها:
    - user_email: ایمیل کاربر
    - user_name: اسم کاربر
    - activation_link: لینک تأیید حساب
    """
    subject = '🎉 به فروشگاه ما خوش آمدید!'
    
    # آماده‌سازی داده‌ها برای قالب
    context = {
        'user_name': user_name,
        'activation_link': activation_link,
    }
    
    # رندر کردن قالب HTML
    html_content = render_to_string('email/welcome.html', context)
    
    # تبدیل HTML به متن ساده (برای ایمیل‌خوان‌های قدیمی)
    text_content = strip_tags(html_content)
    
    from_email = settings.DEFAULT_FROM_EMAIL
    
    try:
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=from_email,
            to=[user_email],
        )
        email.attach_alternative(html_content, "text/html")
        email.send()
        
        logger.info(f"ایمیل خوش‌آمدگویی به {user_email} فرستاده شد")
        return True
    except Exception as e:
        logger.error(f"خطا در ارسال ایمیل خوش‌آمدگویی: {str(e)}")
        return False