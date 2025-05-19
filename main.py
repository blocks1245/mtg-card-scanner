from flask import Flask, render_template_string, send_file, request
import pytesseract
import time
import os
from PIL import Image
import io

USE_OPENCV = False  # 👈 Set to False when running on Raspberry Pi with PiCamera

if USE_OPENCV:
    import cv2
else:
    from picamera import PiCamera

app = Flask(__name__)
IMAGE_PATH = "static/image.jpg"

HTML = """
<!DOCTYPE html>
<html>
<head><title>OCR Camera Viewer</title></head>
<body>
    <h2>Captured Image</h2>
    <img src="/image.jpg?{{ timestamp }}" width="640">
    <h3>Recognized Text:</h3>
    <pre>{{ text }}</pre>
    <form method="POST">
        <button type="submit">Capture Again</button>
    </form>
</body>
</html>
"""

# Setup camera depending on platform
if not USE_OPENCV:
    camera = PiCamera()
    camera.resolution = (640, 480)

def capture_image():
    if USE_OPENCV:
        cap = cv2.VideoCapture(1)
        ret, frame = cap.read()
        if ret:
            cv2.imwrite(IMAGE_PATH, frame)
        cap.release()
    else:
        camera.capture(IMAGE_PATH)

def perform_ocr(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image, config="--psm 6")
    return text.strip()

@app.route('/', methods=["GET", "POST"])
def index():
    capture_image()
    text = perform_ocr(IMAGE_PATH)
    return render_template_string(HTML, text=text, timestamp=int(time.time()))

@app.route('/image.jpg')
def image():
    return send_file(IMAGE_PATH, mimetype='image/jpeg')

if __name__ == '__main__':
    os.makedirs("static", exist_ok=True)
    app.run(host='0.0.0.0', port=5000, debug=False)
