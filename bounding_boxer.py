import cv2

import detection.hand as dh
import detection.object as do

import torch

cap = cv2.VideoCapture(0)
handDetector = dh.HandDetector()
objectDetector = do.ObjectDetector()

tracked = ["bottle", "apple", "carrot"]


def getHandBB(image):
    
    imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    hands = handDetector.getHandBoxes(imageRGB)
    
    for (minx, miny, maxx, maxy) in hands:
        cv2.circle(image, ((minx + maxx) // 2, ((miny + maxy) // 2)), 25, (255, 0, 255), cv2.FILLED)

    return hands, image
    
    
def getObjectBB(image):
    
    imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    boxes = objectDetector.getObjectBoxes(imageRGB)

    results = []

    for box in boxes.iterrows():
        box = box[1]
        #print(box)
        if box["name"] in tracked:
            cx = int((box["xmin"] + box["xmax"]) / 2)
            cy = int((box["ymin"] + box["ymax"]) / 2)

            results.append([box["xmin"], box["ymin"], box["xmax"], box["ymax"]])
            cv2.circle(image, (cx, cy),25, (255, 0, 0), cv2.FILLED)
            
    return results, image
