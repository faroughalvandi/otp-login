# accounts/views.py - کامل و نهایی
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import random
from decouple import config
from django.core.cache import cache
from .models import User

# صفحه ورود (اصلی)
def send_otp(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'login.html')

@csrf_exempt
def send_otp(request):
    if request.method == "POST":
        phone = request.POST.get('phone')
        if not phone or not (phone.startswith('09') and len(phone) == 11):
            return JsonResponse({"error": "شماره موبایل معتبر نیست"}, status=400)

        otp = random.randint(10000, 99999)
        cache.set(f"otp_{phone}", otp, 120)  # ۲ دقیقه اعتبار

        # برای تست: کد رو تو کنسول نشون بده
        print(f"\nکد ورود برای {phone}: {otp}\n")

        # بعداً اینو فعال کن (کاوه‌نگار)
        # try:
        #     requests.get(f"https://api.kavenegar.com/v1/{config('KAVANEGAR_API_KEY')}/verify/lookup.json",
        #                  params={'receptor': phone, 'token': otp, 'template': 'verify'})
        # except: pass

        return JsonResponse({"success": True, "message": "کد ارسال شد"})

    return render(request, 'login.html')

@csrf_exempt
def verify_otp(request):
    if request.method == "POST":
        phone = request.POST.get('phone')
        otp = request.POST.get('otp')
        cached_otp = cache.get(f"otp_{phone}")

        if cached_otp and str(cached_otp) == otp:
            user, created = User.objects.get_or_create(phone=phone)
            if created:
                user.full_name = "کاربر جدید"
                user.save()
                messages.success(request, "خوش آمدی! حساب شما ساخته شد")
            else:
                messages.success(request, "دوباره خوش آمدی!")

            login(request, user)
            cache.delete(f"otp_{phone}")
            return JsonResponse({"success": True, "redirect": "/dashboard/"})
        else:
            return JsonResponse({"error": "کد اشتباه یا منقضی شده"}, status=400)

# داشبورد کاربر (فوق‌العاده زیبا!)
@login_required
def dashboard(request):
    return render(request, 'dashboard.html', {
        'user': request.user
    })

# خروج
def logout_view(request):
    logout(request)
    messages.success(request, "با موفقیت خارج شدید")
    return redirect('login')