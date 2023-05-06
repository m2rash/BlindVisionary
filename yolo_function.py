import pickle
import os

def run_yolo(img_path):
  os.system(f'! python yolov5-master/detect.py --weights yolov5n.pt --img 640 --conf 0.25 --source {img_path}')
  with open('saved_dictionary.pkl', 'rb') as f:
    loaded_dict = pickle.load(f)

  new_dict_with_centers = []
  for element in loaded_dict:
    center = [element[1][0] + element[1][2] // 2, element[1][1] + element[1][3] // 2]
    new_dict_with_centers.append([element[0], center])
  return new_dict_with_centers