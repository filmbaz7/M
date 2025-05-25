# JD Sports Discount Telegram Bot with Webhook

رباتی تلگرام با وب‌هوک که تخفیف‌های بالای ۳۰٪ سایت JD Sports را می‌گیرد و نمایش می‌دهد.

## نصب

1. کلون کردن مخزن:
```bash
git clone https://github.com/yourusername/jd_discount_bot.git
cd jd_discount_bot
```

2. نصب وابستگی‌ها:
```bash
pip install -r requirements.txt
```

3. تنظیم توکن ربات در فایل `app.py`

4. راه‌اندازی وب‌هوک روی سرور با HTTPS (گواهی SSL الزامی است)

## راه‌اندازی وب‌هوک

تلگرام نیاز به URL وب‌هوک با HTTPS دارد. برای ست کردن وب‌هوک، دستور زیر را اجرا کنید:

```bash
curl -F "url=https://YOUR_DOMAIN_OR_IP/YOUR_BOT_TOKEN" https://api.telegram.org/botYOUR_BOT_TOKEN/setWebhook
```

## اجرا

```bash
python app.py
```

---

## نکته

- حتما آدرس صفحه و کلاس‌های HTML را با ساختار واقعی سایت JD Sports تطبیق بده.
- در سرور برای HTTPS می‌توان از Nginx به عنوان reverse proxy استفاده کرد.
