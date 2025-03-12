from flask import Flask, request, jsonify
import cv2
import mediapipe as mp
import numpy as np
from flask_cors import CORS
from hands import detect_hands

app = Flask(__name__)
CORS(app)

mp_hands = mp.solutions.hands.Hands(
    static_image_mode=True, 
    max_num_hands=2,
    min_detection_confidence=0.5
)

@app.route('/detect', methods=['POST'])
def detect():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image received'}), 400

        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No image selected'}), 400

        file = request.files.get('image')
        if not file:
            return jsonify({'error': 'No image received'}), 400

        image_bytes = file.read()

        image_array = np.frombuffer(image_bytes, dtype=np.uint8)
        frame = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

        if frame is None:
            return jsonify({'error': 'Error decoding image'}), 400

        action = detect_hands(frame)

        return jsonify({'action': action})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
