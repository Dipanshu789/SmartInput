from flask import Flask, request, jsonify, render_template
import os
import cv2

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('signup.html')

@app.route('/capture-images', methods=['POST'])
def capture_images():
    user_name = request.json.get('name')
    if not user_name:
        return jsonify({'error': 'Name is required'}), 400

    user_dir = os.path.join('data', user_name)
    os.makedirs(user_dir, exist_ok=True)

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        return jsonify({'error': 'Could not open webcam'}), 500

    for i in range(5):
        ret, frame = cap.read()
        if ret:
            image_path = os.path.join(user_dir, f"{user_name}_{i + 1}.jpg")
            cv2.imwrite(image_path, frame)
        else:
            cap.release()
            return jsonify({'error': 'Failed to capture image'}), 500

    cap.release()
    return jsonify({'message': 'Images captured successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)
