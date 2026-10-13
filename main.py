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
        continue

    # Calculate the absolute difference between the first frame and the current frame
    delta_frame = cv2.absdiff(first_frame, grey_frame_gau)

    # Apply Thresholding: If pixel diff > 30, make it 255 (white)
    # cv2.threshold returns a tuple, we only need the second item [1] which is the actual frame
    thresh_frame = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]

    # Dilate the thresholded frame to smooth out the white blobs
    dil_frame = cv2.dilate(thresh_frame, None, iterations=2)

    # Show the final processed frame
    cv2.imshow("My video", dil_frame)

    key = cv2.waitKey(1)
    if key == ord("q"):
        break

video.release()
cv2.destroyAllWindows()
