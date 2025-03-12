import cv2
import math
import mediapipe as mp

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

def distance_2d(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

cap = cv2.VideoCapture(0)
with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5, max_num_hands=2) as hands:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = hands.process(rgb_frame)

        if results.multi_hand_landmarks and results.multi_handedness:
            hands_info = {}

            # (Left or Right)
            for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
                label = results.multi_handedness[idx].classification[0].label
                hands_info[label] = hand_landmarks

            if "Right" in hands_info and "Left" in hands_info:
                right_hand = hands_info["Right"]
                left_hand = hands_info["Left"]

                # index in right hand
                index_tip = right_hand.landmark[8]
                x_tip, y_tip = int(index_tip.x * w), int(index_tip.y * h)

                # knucles in left hand
                mcp_coords = []
                for mcp_id in [5, 9, 13, 17]:
                    mcp = left_hand.landmark[mcp_id]
                    x_mcp, y_mcp = int(mcp.x * w), int(mcp.y * h)
                    mcp_coords.append((x_mcp, y_mcp))

                # index in right hand
                cv2.circle(frame, (x_tip, y_tip), 5, (0, 255, 0), -1)

                # knucles in left hand
                for i, (x_mcp, y_mcp) in enumerate(mcp_coords):
                    cv2.circle(frame, (x_mcp, y_mcp), 5, (0, 255, 255), -1)

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

        cv2.imshow("Hand Tracking", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
