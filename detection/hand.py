import mediapipe as mp


class HandDetector:
    hands = mp.solutions.hands.Hands()

    def getHandBoxes(self, image): 
        results = self.hands.process(image)

        handBoxes = []

        # checking whether a hand is detected
        if results.multi_hand_landmarks:
            minx, miny = image.shape
            maxx = 0
            maxy = 0
            for handLms in results.multi_hand_landmarks:  # working with each hand
                for id, lm in enumerate(handLms.landmark):
                    h, w, c = image.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)

                    minx = min(cx, minx)
                    miny = min(cy, miny)
                    maxx = max(cx, maxx)
                    maxy = max(cy, maxy)

                    if minx <= maxx and miny <= maxy :
                        handBoxes.append([minx, miny, maxx, maxy])

        return handBoxes
