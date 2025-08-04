import cv2
import mediapipe as mp

class HandPoseDetector:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands()

    def detect_hand_pose(self, image):
        # Convert the image to RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Process the image using MediaPipe Hands
        results = self.hands.process(image_rgb)

        output = []
        if results.multi_hand_landmarks and results.multi_handedness:
            for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                # Get the hand label ("Left" or "Right")
                hand = {}
                label = handedness.classification[0].label
                # Draw landmarks on the image
                for landmark in hand_landmarks.landmark:
                    x = int(landmark.x * image.shape[1])
                    y = int(landmark.y * image.shape[0])
                    z = int(landmark.z * image.shape[1])
                    cv2.circle(image, (x, y), 5, (0, 255, 0), -1)
                # Attach label to the hand landmarks object
                hand["label"] = label
                hand["landmarks"] = hand_landmarks
                output.append(hand)
        return output

def main():
    # Initialize the hand pose detector
    hand_pose_detector = HandPoseDetector()

    # Open a video capture stream (you can replace this with your own image or video input)
    cap = cv2.VideoCapture(1)

    while cap.isOpened():
        # Read a frame from the video stream
        ret, frame = cap.read()

        # Break the loop if the video stream ends
        if not ret:
            break

        # Detect hand pose in the frame
        frame_with_landmarks = hand_pose_detector.detect_hand_pose(frame)

        # Display the frame with hand landmarks
        cv2.imshow("Hand Pose Detector", frame_with_landmarks)

        # Break the loop if the 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture object and close all windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
