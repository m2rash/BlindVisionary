import mediapipe as mp


class HandDetector:
    hands = mp.solutions.hands.Hands()

    def getHandBoxes(self, image): 
        results = self.hands.process(image)

        handBoxes = []

        # checking whether a hand is detected
        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:  # working with each hand
                minx = image.shape[0]
                miny = image.shape[1]
                maxx = 0
                maxy = 0
                for id, lm in enumerate(handLms.landmark):
                    h, w, c = image.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)

                    minx = min(cx, minx)
                    miny = min(cy, miny)
                    maxx = max(cx, maxx)
                    maxy = max(cy, maxy)

                if minx <= maxx and miny <= maxy :
                    handBoxes.append([minx, miny, maxx, maxy])
            mp.solutions.drawing_utils.draw_landmarks(image, handLms, mp.solutions.hands.HAND_CONNECTIONS)

        return handBoxes
