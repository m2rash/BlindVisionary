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


    fingers = handDetector.getIndexLocation(imageRGB)
    #print(boxes)
    for (cx, cy) in fingers:
        cv2.circle(image, (cx, cy), 25, (255, 0, 255), cv2.FILLED)

    boundingBox = fingers # TODO Fix to BB

    return boundingBox, image
    
    
def getObjectBB(image):
    
    imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    
    boxes = objectDetector.getObjectBoxes(imageRGB)
    
    for box in boxes.iterrows():
        box = box[1]
        #print(box)
        if box["name"] in tracked:
            cx = int((box["xmin"] + box["xmax"]) / 2)
            cy = int((box["ymin"] + box["ymax"]) / 2)
            cv2.circle(image, (cx, cy),25, (255, 0, 0), cv2.FILLED)
            
    boundingBox = boxes # TODO fix Marco!!!!
            
    return boundingBox, image
            

    
