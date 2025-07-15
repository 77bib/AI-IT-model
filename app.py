from flask import Flask, jsonify, request
from flask_cors import CORS
import tensorflow as tf
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image
import io

# إعداد التطبيق
app = Flask(__name__)
CORS(app)

# ✅ تحميل النموذج المعدل بصيغة habib.keras
model = load_model('habib.keras')

# إعدادات الصورة
IMG_SIZE = (64, 64)
THRESHOLD = 0.3  # العتبة المستخدمة للتصنيف

def preprocess_image(image):
    if image.mode != 'L':
        image = image.convert('L')
    image = image.resize(IMG_SIZE)
    img_array = np.array(image) / 255.0
    img_array = np.expand_dims(img_array, axis=-1)
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

def predict_image(image):
    img = preprocess_image(image)
    prediction = model.predict(img)[0][0]
    label = "Pneumonia" if prediction > THRESHOLD else "Normal"
    return label, prediction

@app.route('/')
def index():
    return "✅ Binary Chest X-Ray Classification API is running!"

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Empty filename'}), 400

    try:
        image = Image.open(io.BytesIO(file.read()))
        label, confidence = predict_image(image)
        return jsonify({
            'prediction': label,
            'confidence': round(float(confidence), 4)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)
