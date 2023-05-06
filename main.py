import cv2

import detection.hand as dh

cap = cv2.VideoCapture(0)
handDetector = dh.HandDetector()

while True:
    success, image = cap.read()
    imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    fingers = handDetector.getIndexLocation(imageRGB)

    for (cx, cy) in fingers:
        cv2.circle(image, (cx, cy), 25, (255, 0, 255), cv2.FILLED)

    cv2.imshow("Output", image)
    cv2.waitKey(1)
