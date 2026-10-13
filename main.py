import glob
import os
import time
from threading import Thread

import cv2

from emailing import send_email

# 0 targets your default laptop webcam
# Added CAP_DSHOW for instant camera load on Windows
video = cv2.VideoCapture(0, cv2.CAP_DSHOW)
time.sleep(1)

first_frame = None
status_list = [None, None]
count = 1


def clean_folder():
    print("clean folder function started")
    # Added a tiny delay to ensure the email thread has time to open the image
    # before the clean_folder thread deletes it! (Prevents a Race Condition)
    time.sleep(1)
    images = glob.glob("images/*.png")
    for image in images:
        os.remove(image)
    print("clean folder function ended!!!")


while True:
    status = 0
    check, frame = video.read()

    # Flip the frame horizontally to fix the mirrored view
    frame = cv2.flip(frame, 1)

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

    # Find the boundaries of the white shapes
    contours, check = cv2.findContours(
        dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    for contour in contours:
        # If the shape is too small, ignore it (filters out tiny shadows or noise)
        if cv2.contourArea(contour) < 10000:
            continue
        # Get the coordinates to draw a box around the shape
        x, y, w, h = cv2.boundingRect(contour)
        # Draw a green rectangle (0, 255, 0) with a thickness of 3 on the ORIGINAL frame
        rectangle = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0))
        if rectangle.any():
            status = 1
            cv2.imwrite(f"images/{count}.png", frame)
            count = count + 1

    status_list.append(status)
    status_list = status_list[-2:]

    # Trigger Block
    if status_list[0] == 1 and status_list[1] == 0:
        # Calculate the middle image just ONCE when motion ends.
        all_images = glob.glob("images/*.png")
        index = int(len(all_images) / 2)
        image_with_object = all_images[index]

        # Start the email thread
        email_thread = Thread(target=send_email, args=(image_with_object,))
        email_thread.daemon = True
        email_thread.start()

        # start the cleanup thread
        clean_thread = Thread(target=clean_folder)
        clean_thread.daemon = True
        clean_thread.start()

    # print(status_list) --> commented it to stop spamming my terminal. Use it to debug later if you want.
    # Show the original color video, which will now have green boxes drawn on it
    cv2.imshow("Video", frame)

    key = cv2.waitKey(1)
    if key == ord("q"):
        break

video.release()
cv2.destroyAllWindows()
