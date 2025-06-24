# استخدم صورة بايثون 3.10
FROM python:3.10-slim

# تعيين مجلد العمل داخل الحاوية
WORKDIR /app

# نسخ الملفات
COPY . .

# تثبيت المتطلبات
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# فتح المنفذ
EXPOSE 10000

# أمر التشغيل
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "app:app"]
