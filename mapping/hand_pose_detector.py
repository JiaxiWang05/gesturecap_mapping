from hand_pose_detector import HandPoseDetector
import cv2
from pythonosc import udp_client
import time
import math

# Initialise hand pose detector and video capture
detector = HandPoseDetector()
cap = cv2.VideoCapture(0)
# cap = cv2.VideoCapture("/dev/video2")

# Initialise OSC client
osc_ip = "127.0.0.1"
osc_port = 11111
client = udp_client.SimpleUDPClient(osc_ip, osc_port)

fps = 60
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
            else:
                continue
                
            if hand_label == "left":
                left_index_pos = landmarks[8]
                left_thumb_pos = landmarks[4]
                distance = math.dist([left_index_pos.x, left_index_pos.y],
                                     [left_thumb_pos.x, left_thumb_pos.y])
                
                # Send left hand coordinates
                client.send_message("/LHX", left_index_pos.x)
                client.send_message("/LHY", left_index_pos.y)
                
                # Left hand tap logic (same as before)
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
                
                # Send right hand coordinates
                client.send_message("/RHX", right_index_pos.x)
                client.send_message("/RHY", right_index_pos.y)
                
                # Right hand logic remains the same for latency measurement
                if distance < 0.1:
                    play_start_time = time.time()
                    play_end_time = time.time()
                    audio_output_latency = (play_end_time - play_start_time) * 1000

                    total_latency = (play_end_time - total_start_time) * 1000
                    total_latency_array.append(total_latency)
                    frame_latency_array.append(frame_input_latency)
                    processing_latency_array.append(processing_latency)
                    audio_latency_array.append(audio_output_latency)

    trig_val = 0

    # Send trigger for left hand tap (same logic as before)
    if left_hand_tapped:
        trig_val = 1
        client.send_message("/trigger", trig_val)

    cv2.imshow("Hand Pose", frame)

    if cv2.waitKey(delay) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
