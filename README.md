# Motion Alert App (Python Computer Vision) 👩🏻‍💻📸

A lightweight, multi-threaded computer vision application that transforms a standard webcam into a smart security monitor. It detects motion, tracks object state, captures the optimal frame, and dispatches an email alert with the image attached, all in real-time without interrupting the video feed.

## Features

- **Real-Time Motion Detection:** Utilizes OpenCV for grayscale conversion, Gaussian blurring, and contour mapping to track moving objects.
- **Smart State Tracking:** Employs a sliding-window algorithm to track object presence and trigger alerts only when an object fully exits the frame, ensuring the best possible capture.
- **Multi-Threaded Architecture:** Offloads SMTP network requests and file I/O operations to background threads, preventing the OpenCV video loop from freezing during email dispatch.
- **Automated Storage Management:** A dedicated cleanup thread purges temporary capture files after successful transmission to prevent memory overflow.
- **Secure Credential Management:** Utilizes `python-dotenv` to keep sensitive SMTP passwords and email addresses completely out of the source code.

## Tech Stack

- **Language:** Python 3
- **Computer Vision:** OpenCV (`opencv-python`)
- **Concurrency:** `threading` (Standard Library)
- **Environment Management:** `uv`, `python-dotenv`
