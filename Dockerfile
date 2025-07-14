# استخدم Python 3.10 وصورة تدعم TensorFlow 2.13
FROM python:3.10-slim

WORKDIR /app

# انسخ ملفات المشروع
COPY . .

# ثبّت tensorflow مع الإصدار المطلوب
RUN pip install --upgrade pip && \
    pip install tensorflow==2.13.0 && \
    pip install -r requirements.txt

EXPOSE 10000

CMD ["gunicorn", "--bind", "0.0.0.0:10000", "app:app"]

