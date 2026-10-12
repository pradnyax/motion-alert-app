import time

import cv2

# 0 targets your default laptop webcam
video = cv2.VideoCapture(0)
time.sleep(1)

while True:
    check, frame = video.read()

    # step1: convert the frame to greyscale
    grey_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # step2: blur the greyscale frame
    # (21,21) is the blur intensity and 0 is the standard deviation.
    grey_frame_gau = cv2.GaussianBlur(grey_frame, (21, 21), 0)

    # Show the processed frame instead of the raw color one
    cv2.imshow("My video", grey_frame_gau)

    key = cv2.waitKey(1)

    if key == ord("q"):
        break

video.release()
cv2.destroyAllWindows()
