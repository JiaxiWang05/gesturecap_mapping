from hand_pose_detector import HandPoseDetector
import cv2
from pythonosc import udp_client
import time
import math

# Initialize hand pose detector and video capture
detector = HandPoseDetector()
cap = cv2.VideoCapture(0)
# cap = cv2.VideoCapture("/dev/video2")

# Initialize OSC client
osc_ip = "127.0.0.1"
osc_port = 11111
client = udp_client.SimpleUDPClient(osc_ip, osc_port)

fps = 200
delay = int(1000 / fps)

state = 0  # For left hand tap logic
counter = 0

total_latency_array = []
frame_latency_array = []
processing_latency_array = []
audio_latency_array = []

while cap.isOpened():
    total_start_time = time.time()
    
    # Frame capture time
    frame_start_time = time.time()
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    frame_end_time = time.time()
    frame_input_latency = (frame_end_time - frame_start_time) * 1000

    if not ret:
        break

    # Hand pose detection time
    process_start_time = time.time()
    hands = detector.detect_hand_pose(frame)
    process_end_time = time.time()
    processing_latency = (process_end_time - process_start_time) * 1000

    left_hand_tapped = False

    if hands:
        for hand in hands:
            landmarks = hand["landmarks"].landmark

            # Use the label provided by the detector ("Left" or "Right")
            if "label" in hand:
                hand_label = hand["label"].lower()
                # print("detected handedness")
            else:
                continue
            volume = 0
            if hand_label == "left":
                left_index_pos = landmarks[8]
                left_thumb_pos = landmarks[4]
                distance = math.dist([left_index_pos.x, left_index_pos.y],
                                     [left_thumb_pos.x, left_thumb_pos.y])
                # Left hand tap logic
                if distance >= 0.08 and state == 1:
                    state = 0
                elif distance < 0.08 and state == 0:
                    state = 1
                
                    left_hand_tapped = True
                    counter += 1
                    print("Left hand counter:", counter)
            elif hand_label == "right":
                right_index_pos = landmarks[8]
                right_thumb_pos = landmarks[4]
                distance = math.dist([right_index_pos.x, right_index_pos.y],
                                     [right_thumb_pos.x, right_thumb_pos.y])
                # Right hand logic remains the same
                if distance < 0.1:
                    play_start_time = time.time()
                    # freq = 100000 / ((right_index_pos.x ** 2) * 1000 + 100)
                    # freq = 1000 / ((right_index_pos.x ** 2) * 1000 + 100)
                    freq = right_index_pos.x
                    min_val = -2.0
                    max_val = 7
                    mapped_freq = min_val + (max_val - min_val) * freq

                    # print(freq)
                    volume = right_index_pos.y
                    min_c = 1000
                    max_c = 7000
                    mapped_volume = min_c + (max_c - min_c) * volume

                    client.send_message("/q", mapped_freq)
                    client.send_message("/c", mapped_volume)

                    play_end_time = time.time()
                    audio_output_latency = (play_end_time - play_start_time) * 1000

                    total_latency = (play_end_time - total_start_time) * 1000
                    total_latency_array.append(total_latency)
                    frame_latency_array.append(frame_input_latency)
                    processing_latency_array.append(processing_latency)
                    audio_latency_array.append(audio_output_latency)

    trig_val = 0

    # Send a single OSC trigger for left hand tap
    if left_hand_tapped:
        trig_val = 1
        client.send_message("/trigger", trig_val)
    # print(trig_val)

    cv2.imshow("Hand Pose", frame)

    if cv2.waitKey(delay) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
