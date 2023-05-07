import cv2

import detection.hand as dh
import detection.object as do

import torch
import numpy as np

cap = cv2.VideoCapture(0)
handDetector = dh.HandDetector()
objectDetector = do.ObjectDetector()

#tracked = ["bottle", "apple", "carrot"]
tracked = ["apple"]

def getHandBB(image):
    
    imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    hands = handDetector.getHandBoxes(imageRGB)

    #for (minx, miny, maxx, maxy) in hands:
        #cv2.circle(image, ((minx + maxx) // 2, ((miny + maxy) // 2)), 25, (255, 0, 255), cv2.FILLED)
        #cv2.rectangle(imageRGB, (minx, miny), (maxx, maxy), (255, 0, 255), 4)
    return hands, cv2.cvtColor(imageRGB, cv2.COLOR_RGB2BGR)
    
    
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

            results.append([int (box["xmin"]), int (box["ymin"]), int (box["xmax"]), int (box["ymax"])])
            cv2.circle(image, (cx, cy),25, (255, 0, 0), cv2.FILLED)
            
    return results, image


def getMockBB(image):
    
    imageRGB = image
    
    qcd = cv2.QRCodeDetector()
    
    ret_qr, decoded_info, points, _ = qcd.detectAndDecodeMulti(imageRGB)
    results = []
    if ret_qr:
        for p in (points):
            imageRGB = cv2.polylines(imageRGB, [p.astype(int)], True, (0,0,255), 8)
    
        results = (int(points[0][0][0]), int(points[0][0][1]), int(points[0][-1][0]), int(points[0][-1][1]))

    
    return results, imageRGB

def getMockBB(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Blur using 3 * 3 kernel.
    gray_blurred = cv2.medianBlur(gray, 5)

    # Apply Hough transform on the blurred image.
    detected_circles = cv2.HoughCircles(gray_blurred, 
                    cv2.HOUGH_GRADIENT, 1, 20, param1 = 100,
                param2 = 30, minRadius = 10, maxRadius = 100)
    
    results = []
    if detected_circles is not None:

        # Convert the circle parameters a, b and r to integers.
        detected_circles = np.uint16(np.around(detected_circles))

        for pt in detected_circles[0, :]:
            a, b, r = pt[0], pt[1], pt[2]
            print(image.shape)
            if image[min(a, image.shape[0] - 1)][min(b, image.shape[1] - 1)][1] > 40:
                print(image[min(a, image.shape[0] - 1)][min(b, image.shape[1] - 1)][1])
                results = (a - r, b - r, a+ r, b+ r)
                # Draw the circumference of the circle.
                cv2.circle(image, (a, b), r, (0, 255, 0), 2)
                # Draw a small circle (of radius 1) to show the center.
                cv2.circle(image, (a, b), 1, (0, 0, 255), 3)
    
    return results, image 
