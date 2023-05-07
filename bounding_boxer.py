import cv2

import detection.hand as dh
# import detection.object as do

import torch

cap = cv2.VideoCapture(0)
handDetector = dh.HandDetector()
# objectDetector = do.ObjectDetector()

tracked = ["bottle", "apple", "carrot"]


def getHandBB(image):
    
    imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    hands = handDetector.getHandBoxes(imageRGB)

    for (minx, miny, maxx, maxy) in hands:
        #cv2.circle(image, ((minx + maxx) // 2, ((miny + maxy) // 2)), 25, (255, 0, 255), cv2.FILLED)
        cv2.rectangle(image, (minx, miny), (maxx, maxy), (255, 0, 255), 4)
    return hands, image
    
    
# def getObjectBB(image):
    
#     imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#     boxes = objectDetector.getObjectBoxes(imageRGB)

#     results = []

#     for box in boxes.iterrows():
#         box = box[1]
#         #print(box)
#         if box["name"] in tracked:
#             cx = int((box["xmin"] + box["xmax"]) / 2)
#             cy = int((box["ymin"] + box["ymax"]) / 2)

#             results.append([int (box["xmin"]), int (box["ymin"]), int (box["xmax"]), int (box["ymax"])])
#             cv2.circle(image, (cx, cy),25, (255, 0, 0), cv2.FILLED)
            
#     return results, image

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
