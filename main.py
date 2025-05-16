import cv2
import easyocr

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'], gpu=True)

# Open camera (adjust index if needed)
cap = cv2.VideoCapture(1)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Resize for consistent processing
    frame = cv2.resize(frame, (800, int(frame.shape[0] * 800 / frame.shape[1])))
    h, w = frame.shape[:2]

    # Define central rectangle
    rect_w, rect_h = int(w * 0.2), int(h * 0.1)
    x1, y1 = (w - rect_w) // 2, (h - rect_h) // 2
    x2, y2 = x1 + rect_w, y1 + rect_h

    # Extract Region of Interest (ROI)
    roi = frame[y1:y2, x1:x2]

    # Run OCR only on ROI
    results = reader.readtext(roi)

    # Draw rectangle on main frame
    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # Display OCR results below the rectangle
    for i, (_, text, _) in enumerate(results):
        cv2.putText(frame, text, (x1, y2 + 25 + i * 25),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    # Show the final output
    cv2.imshow("Text Overlay with OCR", frame)

    if cv2.waitKey(5) & 0xFF == 27:  # ESC to quit
        break

cap.release()
cv2.destroyAllWindows()
