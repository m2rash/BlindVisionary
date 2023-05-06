import mediapipe as mp


class HandDetector:
    hands = mp.solutions.hands.Hands()

    def getIndexLocation(self, image):
        results = self.hands.process(image)

        fingers = []

        # checking whether a hand is detected
        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:  # working with each hand
                for id, lm in enumerate(handLms.landmark):
                    h, w, c = image.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)

                    if id == 8:
                        fingers.append((cx, cy))

        return fingers
