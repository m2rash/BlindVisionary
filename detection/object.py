import torch


class ObjectDetector:
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

    def getObjectBoxes(self, image):
        # Inference
        results = self.model(image)

        return results.pandas().xyxy[0]
