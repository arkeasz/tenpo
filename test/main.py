import cv2
import mediapipe as mp
import math

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

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
            for hand, hand_landmarks in enumerate(results.multi_hand_landmarks):
                h, w, _ = frame.shape

                finger_tips = [4, 8]
                finger_mcp = [2, 5]
                d = []
                fi = ()


                for i in range(2):
                    finger_index = i + hand*2
                    tip = hand_landmarks.landmark[finger_tips[i]]
                    mcp = hand_landmarks.landmark[finger_mcp[i]]


                    x_cord = int(tip.x * w)
                    y_cord = int(tip.y * h)
                    z_cord = tip.z

                    d.append(x_cord)
                    d.append(y_cord)
                    d.append(z_cord)
                    fi = (x_cord, y_cord)
                    frame = cv2.circle(frame, (x_cord, y_cord), 5, (0, 255, 0), -1)

                if len(d) == 6: # coords: (x1, y1, z1, x2, y2, z2)
                    result_distance = math.sqrt((d[0] - d[3])**2 + (d[1] - d[4])**2 + (d[2] - d[5])**2)
                    frame = cv2.putText(frame, f"Distancia: {int(result_distance)}", (fi[0] + 10, fi[1] + 10), cv2.FONT_HERSHEY_SIMPLEX, .5, (255, 100, 100), 2)

                    thumb_x, thumb_y = d[0], d[1]
                    index_x, index_y = d[3], d[4]
                    frame = cv2.line(frame, (thumb_x, thumb_y), (index_x, index_y), (255, 0, 0), 2)

                    if result_distance < CLIC_THRESHOLD:
                        cv2.putText(frame, "YOU DID IT!", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)


        cv2.imshow('Hand detection', frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()
