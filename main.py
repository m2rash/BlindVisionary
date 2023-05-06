import cv2

import detection.hand as dh
import detection.object as do

import torch

cap = cv2.VideoCapture(0)
handDetector = dh.HandDetector()
objectDetector = do.ObjectDetector()

tracked = ["bottle", "apple", "carrot"]

while True:
    success, image = cap.read()
    imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    #gray = cv2.resize(imageRGB, [imageRGB.shape[0] // 2, imageRGB.shape[1] // 2], interpolation = cv2.INTER_AREA)

    fingers = handDetector.getIndexLocation(imageRGB)
    boxes = objectDetector.getObjectBoxes(imageRGB)
    #print(boxes)
    for (cx, cy) in fingers:
        cv2.circle(image, (cx, cy), 25, (255, 0, 255), cv2.FILLED)

    for box in boxes.iterrows():
        box = box[1]
        #print(box)
        if box["name"] in tracked:
            cx = int((box["xmin"] + box["xmax"]) / 2)
            cy = int((box["ymin"] + box["ymax"]) / 2)
            cv2.circle(image, (cx, cy),25, (255, 0, 0), cv2.FILLED)
        #print(box.name)

    cv2.imshow("Output", image)
    cv2.waitKey(1)
