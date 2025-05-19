import cv2
import pytesseract
from flask import Flask, Response, render_template_string
import threading

# Initialize Flask app
app = Flask(__name__)

# OpenCV camera
cap = cv2.VideoCapture(0)

# Simple HTML template to show stream
HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Pi OCR Stream</title>
</head>
<body>
    <h2>OCR Live Stream from Raspberry Pi</h2>
    <img src="{{ url_for('video_feed') }}" width="640" />
</body>
</html>
"""

def generate_frames():
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Resize for performance
        frame = cv2.resize(frame, (640, 360))
        h, w = frame.shape[:2]

        # Define central ROI
        rect_w, rect_h = int(w * 0.3), int(h * 0.1)
        x1, y1 = (w - rect_w) // 2, (h - rect_h) // 2
        x2, y2 = x1 + rect_w, y1 + rect_h
        roi = frame[y1:y2, x1:x2]

        # Preprocess ROI
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

        # Run OCR
        text = pytesseract.image_to_string(thresh, config='--psm 6')

        # Draw rectangle and OCR result
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        y_text = y2 + 25
        for line in text.strip().split('\n'):
            if line.strip():
                cv2.putText(frame, line.strip(), (x1, y_text), cv2.FONT_HERSHEY_SIMPLEX,
                            0.6, (0, 255, 0), 2)
                y_text += 25

        # Encode frame as JPEG
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        # Yield to browser as multipart
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

def run_flask():
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)

if __name__ == '__main__':
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()
