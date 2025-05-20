import time
import cv2
import numpy as np
from PIL import Image
import pytesseract
from picamera2 import Picamera2

def initialize_camera():
    picam2 = Picamera2()
    picam2.configure(picam2.create_still_configuration(main={"size": (640, 480)}))
    picam2.start()
    time.sleep(2)  # Camera warm-up
    return picam2

def capture_and_ocr(picam2):
    frame = picam2.capture_array()
    pil_image = Image.fromarray(frame)
    text = pytesseract.image_to_string(pil_image, config="--psm 6").strip()
    return frame, text

def display_image_with_text(frame, text):
    # Draw text lines
    y0, dy = 30, 30
    for i, line in enumerate(text.splitlines()):
        y = y0 + i * dy
        cv2.putText(frame, line, (10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    # Display image
    cv2.imshow("OCR Result", frame)
    cv2.waitKey(0)  # Wait for key press to close
    cv2.destroyAllWindows()

def main():
    print("OCR Camera Ready. Press Enter to capture. Ctrl+C to exit.")
    picam2 = initialize_camera()

    try:
        while True:
            input("Press Enter to capture image and perform OCR...")
            frame, text = capture_and_ocr(picam2)
            print("Recognized Text:\n" + text)
            display_image_with_text(frame, text)
    except KeyboardInterrupt:
        print("\nExiting.")
    finally:
        picam2.stop()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
