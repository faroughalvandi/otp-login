## ویژگی‌ها
- ورود فقط با شماره موبایل
- ارسال پیامک واقعی (کاوه‌نگار)
- طراحی مدرن، ریسپانسیو و تماماً فارسی (Tailwind CSS)
- بدون رفرش صفحه (AJAX)
- داشبورد کاربر خفن
- امنیت بالا + محدودیت زمانی کد

## نصب و راه‌اندازی سریع

```bash
git clone https://github.com/faroughalvandi/otp-login
cd otp-login
pip install -r requirements.txt

##فعال کردن کاوه‌نگار ۱۰۰٪ واقعی (حتماً انجام بده)
مرحله ۱: ساخت قالب در پنل کاوه‌نگار

وارد پنل شو: https://panel.kavenegar.com
برو به: سرویس‌ها → اعتبارسنجی (Verify)
یه قالب جدید بساز با این متن دقیق:textکد ورود شما: {token}
اسم قالب رو بذار: otp_login
ارسال کن و منتظر تأیید باش (معمولاً ۱–۴ ساعت، گاهی همون لحظه تأیید می‌شه)

مرحله ۲: تنظیم فایل .env
فایل .env.example رو کپی کن و اسمش رو بذار .env:
envSECRET_KEY=super-secret-change-in-production-1404
DEBUG=True

# کاوه‌نگار - کلید خودت رو وارد کن
KAVANEGAR_API_KEY=خودتون
KAVANEGAR_TEMPLATE=otp_login

فقط این تابع رو تو accounts/views.py عوض کن (بقیه کد همون قبلی)

@csrf_exempt
def send_otp(request):
    if request.method == "POST":
        phone = request.POST.get('phone')
        if not phone or not (phone.startswith('09') and len(phone) == 11):
            return JsonResponse({"error": "شماره موبایل معتبر نیست"}, status=400)

        otp = random.randint(10000, 99999)
        cache.set(f"otp_{phone}", otp, 120)  # ۲ دقیقه

        # ارسال واقعی با کاوه‌نگار
        try:
            import requests
            url = f"https://api.kavenegar.com/v1/{config('KAVANEGAR_API_KEY')}/verify/lookup.json"
            payload = {
                'receptor': phone,
                'token': otp,
                'template': config('KAVANEGAR_TEMPLATE', 'otp_login')
            }
            response = requests.get(url, params=payload, timeout=10)
            
            if response.status_code == 200:
                print(f"پیامک واقعی ارسال شد به {phone} | کد: {otp}")
                return JsonResponse({"success": True, "message": "کد ارسال شد"})
            else:
                print("خطا در ارسال پیامک:", response.text)
                return JsonResponse({"error": "خطا در ارسال پیامک"}, status=500)
                
        except Exception as e:
            print("خطای اتصال به کاوه‌نگار:", e)
            return JsonResponse({"error": "خطا در ارسال پیامک"}, status=500)

    return render(request, 'login.html')
