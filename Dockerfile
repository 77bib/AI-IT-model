# استخدم صورة Python الحديثة المتوافقة مع TensorFlow 2.13
FROM python:3.10-slim

# إعداد مجلد العمل داخل الحاوية
WORKDIR /app

# نسخ كل ملفات المشروع إلى الحاوية
COPY . .

# تحديث pip وتثبيت المتطلبات
RUN pip install --upgrade pip && \
    pip install tensorflow==2.13.0 && \
    pip install -r requirements.txt

# فتح المنفذ الذي سيعمل عليه التطبيق
EXPOSE 10000

# أمر تشغيل التطبيق باستخدام gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "app:app"]
