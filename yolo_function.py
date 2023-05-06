import pickle
import os
import cv2

import yolov5master.detect as det


def run_yolo(img):
    det.run(weights='yolov5n.pt', source=img)
    with open('saved_dictionary.pkl', 'rb') as f:
        loaded_dict = pickle.load(f)

    new_dict_with_centers = []
    for element in loaded_dict:
        center = [element[1][0] + element[1][2] //
                  2, element[1][1] + element[1][3] // 2]
        new_dict_with_centers.append([element[0], center])
    return new_dict_with_centers


print(run_yolo("newtest.jpg"))
