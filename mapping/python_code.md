 
# Hand Pose Detection to OSC Streaming

This project implements hand pose detection using a camera and streams the hand's position coordinates (left and right index finger) coordinates (x, y) via OSC (Open Sound Control) messages. The script has been adapted from Deepansh's `doublehand.py` for gesture detection and data streaming, focusing on transmitting hand position data instead of audio parameters.

 
 

## Setup and Installation
see the other readme file. 


⸻

Code Overview

	•	Initialise Detector & Video Capture: Using cv2.VideoCapture(0) to capture video from the webcam.
	•	OSC Setup: Configure the OSC UDP client to send messages to 127.0.0.1 on port 11111.
	•	Frame Rate Control: Using fps and delay to control the frame rate, with the latest version using a frame rate of 60 FPS ( not a very effect change) (hope to  reduces system strain and aims for more stable performance. The delay calculation adjustment is reflected accordingly, though no major improvements were observed.) 

Data Flow
	1.	Hand Position → Raw Data
	2.	OSC Stream → External Processing(Max)
OSC Streaming: After detecting the position of the left and right index fingers(Landmark 8), their x and y coordinates are sent as OSC messages （Left Hand Coordinates: /LHX, /LHY）	（Right Hand Coordinates: /RHX, /RHY）

 Here is the list of possible vocabulary that need to be finalised before 8th August 
#### Skeletal Joint Coordinates (Linked to MediaPipe Landmarks (33 pose landmarks https://www.mdpi.com/2076-3417/13/4/2700)

# Hand Pose Detection to OSC Streaming ( list of input from Martin's Patch) 

 
![Alt Text](https://www.mdpi.com/applsci/applsci-13-02700/article_deploy/html/images/applsci-13-02700-g001.png)

# Hand gesture Detection to OSC Streaming
![Image Alt Text](https://mediapipe.dev/images/mobile/hand_landmarks.png)

client.send_message("/LHX", left_index_pos.x). This is the action that takes the wanted x and y coordinates in each iteration of the loop and sends them out over the network via OSC.You do not need to define left_index_pos.x yourself. It comes with MediaPipe as part of the data structure it returns.
