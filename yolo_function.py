
import pickle
import cv2
import sys

YOLO_ROOT = 'C:/Users/marco/Documents/Hackathon/Zeiss23/yolov5master'
if YOLO_ROOT not in sys.path:
    sys.path.append(YOLO_ROOT)  # add ROOT to PATH

import yolov5master.detect as det

def run_yolo(img_file):
    det.run(weights='yolov5s.pt', source=img_file, conf_thres=0.12)
    with open('saved_dictionary.pkl', 'rb') as f:
        loaded_dict = pickle.load(f)

    new_dict_with_centers = []
    for element in loaded_dict:
        center = [(element[1][0] + element[1][2]) //
                  2, (element[1][1] + element[1][3]) // 2]
        new_dict_with_centers.append([element[0], center])
    return new_dict_with_centers


def detectBoxes(img):
    img_file = "temp.jpg"
    cv2.imwrite(img_file, img)
    return run_yolo(img_file)


#print(run_yolo("hello.jpeg"))
