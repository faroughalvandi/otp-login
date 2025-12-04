# core/urls.py
from django.contrib import admin
from django.urls import path
from django.contrib.auth.decorators import login_required
from accounts.views import send_otp, verify_otp, dashboard, logout_view

urlpatterns = [
    path('admin/', admin.site.urls),

    # صفحه اصلی: ورود با OTP
    path('', send_otp, name='login'),                 # http://127.0.0.1:8000/
    path('send-otp/', send_otp, name='send_otp'),
    path('verify-otp/', verify_otp, name='verify_otp'),

    # داشبورد کاربر (فقط برای لاگین شده‌ها)
    path('dashboard/', login_required(dashboard), name='dashboard'),

    # خروج
    path('logout/', logout_view, name='logout'),
]