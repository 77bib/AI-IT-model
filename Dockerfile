# استخدم نسخة خفيفة من Python 3.10
FROM python:3.10-slim

# تعيين مجلد العمل داخل الحاوية
WORKDIR /app

# نسخ جميع ملفات المشروع إلى الحاوية
COPY . .

# تثبيت المتطلبات
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# فتح المنفذ المطلوب
EXPOSE 10000

# تشغيل التطبيق باستخدام gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "app:app"]
