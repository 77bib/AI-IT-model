from flask import Flask, jsonify, request
from flask_cors import CORS
import tensorflow as tf
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image
import io

app = Flask(__name__)
CORS(app)  # <== مهم جدًا لحل مشكلة CORS

# تحميل النموذج الثنائي
model = load_model('binairy.h5')

def predict_image(image):
    # تحويل الصورة إلى صورة رمادية
    if image.mode != 'L':
        image = image.convert('L')
    
    # تغيير حجم الصورة إلى 64x64 (حسب النموذج الجديد)
    image = image.resize((64, 64))
    
    # تحويل الصورة إلى مصفوفة
    image_array = np.array(image) / 255.0
    
    # إضافة بعد القناة (64, 64, 1)
    image_array = np.expand_dims(image_array, axis=-1)
    
    # إضافة بعد الدفعة (1, 64, 64, 1)
    image_array = np.expand_dims(image_array, axis=0)
    
    # التنبؤ
    prediction = model.predict(image_array)
    
    # تحويل التنبؤ إلى فئة (Normal أو Pneumonia)
    threshold = 0.3  # نفس العتبة المستخدمة في التدريب
    predicted_class = 'Pneumonia' if prediction[0][0] > threshold else 'Normal'
    
    return predicted_class, prediction[0][0]

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'لا يوجد ملف'}), 400
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'لم يتم اختيار ملف'}), 400
    
    try:
        # تحويل الصورة المرفوعة إلى صورة باستخدام PIL
        image = Image.open(io.BytesIO(file.read()))
        prediction, confidence = predict_image(image)
        
        return jsonify({
            'prediction': prediction,
            'confidence': float(confidence)
        })
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/')
def home():
    return "مرحباً بك في مختبر الذكاء الاصطناعي"

if __name__ == '__main__':
    app.run(debug=True, port=5001)