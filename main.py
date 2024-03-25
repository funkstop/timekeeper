from detection import detect_clock
from analysis import tell_time
import cv2

# Open the default camera
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open camera")
    exit(1)

while True:
    # Capture frame-by-frame
    ret, img = cap.read()

    if not ret:
        print("Error: Could not read frame")
        break

    bbox = detect_clock(img)

    if bbox is not None:
        img_boxed = img.copy()
        cv2.rectangle(img_boxed, (bbox[0], bbox[1]),
                      (bbox[2], bbox[3]), (255, 0, 0), 5)
        img_boxed = cv2.putText(img_boxed, "clock", (
            bbox[0], bbox[3]), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2, bottomLeftOrigin=False)

        cv2.imshow('clock', img_boxed)
        cv2.waitKey(0)  # Wait for a key input after detection


        clock = img[bbox[1]:bbox[3], bbox[0]:bbox[2]]
        clock = cv2.resize(clock, (400, 400))

        cv2.imshow('clock', clock)
        cv2.waitKey(0)

        hours, minutes = tell_time(clock)

        time_string = f"{hours}:{minutes:02}"
        cv2.putText(clock, time_string, (220, 380),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 50, 50), 6)
        cv2.rectangle(clock, (0, 0), (400, 400), (0, 0, 0), 3)

        print(time_string)

        cv2.imshow("clock", clock)
        cv2.waitKey(0)  # Wait for a key input after detection

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
cap.release()
cv2.destroyAllWindows()