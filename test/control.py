import cv2
import mediapipe as mp
import math

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

def distance_2d(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

cap = cv2.VideoCapture(0)
CLIC_THRESHOLD = 30

with mp_hands.Hands(min_detection_confidence = 0.5, min_tracking_confidence = 0.5, max_num_hands = 2) as Hands:
    finger_state = [False]*6

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break;

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = Hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            landmarks_by_hand = []
            for hand_landmarks in results.multi_hand_landmarks:
                landmarks_by_hand.append(hand_landmarks)

            if len(landmarks_by_hand) == 2:
                h, w, _ = frame.shape
                hand1, hand2 = landmarks_by_hand
                index_tip = hand1.landmark[8]
                x_tip, y_tip = int(index_tip.x * w), int(index_tip.y * h)

                fingers_mcp = [5, 9, 13, 17]

                mcp_coords = []
                for mcp_id in fingers_mcp:
                    mcp = hand2.landmark[mcp_id]
                    x_mcp, y_mcp = int(mcp.x * w), int(mcp.y * h)
                    mcp_coords.append((x_mcp, y_mcp))

                cv2.circle(frame, (x_tip, y_tip), 5, (0, 255, 0), -1)

                for i, (x_mcp, y_mcp) in enumerate(mcp_coords):
                    cv2.circle(frame, (x_mcp, y_mcp), 5, (0, 255, 255), -1)
                    cv2.line(frame, (x_tip, y_tip), (x_mcp, y_mcp), (255, 0, 0), 2)

                    distance = distance_2d((x_tip, y_tip), (x_mcp, y_mcp))
                    if distance < 15:
                        finger = ''
                        if i == 0:
                            finger = 'index'
                        if i == 1:
                            finger = 'middle'
                        if i == 2:
                            finger = 'ring'
                        if i == 3:
                            finger = 'pinky'

                        cv2.putText(frame, "Touching - " + finger, (x_tip, y_tip - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        cv2.imshow('Hand detection', frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()
