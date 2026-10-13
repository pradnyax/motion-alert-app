import time

import cv2

# 0 targets your default laptop webcam
video = cv2.VideoCapture(0)
time.sleep(1)

first_frame = None

while True:
    check, frame = video.read()

    # step1: convert the frame to greyscale
    grey_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # step2: blur the greyscale frame
    # (21,21) is the blur intensity and 0 is the standard deviation.
    grey_frame_gau = cv2.GaussianBlur(grey_frame, (21, 21), 0)

    if first_frame is None:
        first_frame = grey_frame_gau

    # Calculate the absolute difference between the first frame and the current frame
    delta_frame = cv2.absdiff(first_frame, grey_frame_gau)

    # show the difference frame
    cv2.imshow("My video", delta_frame)

    key = cv2.waitKey(1)
    if key == ord("q"):
        break

video.release()
cv2.destroyAllWindows()
