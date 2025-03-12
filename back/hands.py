import cv2
import mediapipe as mp
import math

mp_hands = mp.solutions.hands.Hands(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5,
    max_num_hands=2
)

CLIC_THRESHOLD = 30

def detect_hands(frame):
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = mp_hands.process(rgb_frame)
    action = ''
    dis = 0

    if results.multi_hand_landmarks:
        h, w, _ = frame.shape
        finger_tips = [4, 8]
        points = []


        for hand_landmarks in results.multi_hand_landmarks:
            for tip_id in finger_tips:
                tip = hand_landmarks.landmark[tip_id]
                x_cord, y_cord = int(tip.x * w), int(tip.y * h)
                points.append((x_cord, y_cord))

            if len(points) == 2:
                x1, y1 = points[0]
                x2, y2 = points[1]
                result_distance = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

                if result_distance < CLIC_THRESHOLD:
                    action = 'clic'
                dis = result_distance

    return (action, dis)
