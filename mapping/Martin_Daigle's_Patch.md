# Gesture-Based Music Control System

**Control Ableton Live, synthesisers, and musical tools like audio effects( delay, reverb etc) with hand gestures in real-time.**

## Demo

> *Real-time gesture control demonstration using Rick Astley's "Never Gonna Give You Up" separated tracks to showcase individual parameter control*
> 

[![Gesture-Based Music Control System Demo](https://img.youtube.com/vi/aJl4vnLZrYE/maxresdefault.jpg)](https://www.youtube.com/watch?v=aJl4vnLZrYE)

**[Watch Full Demo](https://youtu.be/aJl4vnLZrYE)** 

 ## Audio Sample Attribution

This demonstration uses six separated tracks from Rick Astley's **"Never Gonna Give You Up"** for testing the gesture control system. The individual track stems allow viewers to hear how different musical elements (drums, bass, vocals, etc.) respond to hand gestures.

**Source**: Rick Astley - Never Gonna Give You Up  
  

### Individual Track Names:[Find the sample track here]()
- **Track 1**: Drums/Percussion
- **Track 2**: Bass
- **Track 3**: Lead Vocals
- **Track 4**: Background 
- **Track 5**: Keyboard 
- **Track 6**: Guitar 

This audio is used for educational and demonstration purposes only to showcase the real-time gesture control capabilities of the system. All rights to the original composition belong to Rick Astley and respective copyright holders.
 

## Overview

This system tracks hand movements and converts them into real-time control messages and gives **gesture-based control** over parameter in Ableton Live.

**Credit**:This is a simplified version of martin daigle's gesture control patch M4LMapBack for using a simpler and less sophisticated approach.

## Key Features


- **Real-time hand tracking** via computer's webcam or external camera
- **low latency** performance for live music
- **Modular design** - control one parameter in one batch and customisable.
- **Direct Ableton Live integration** via Max for Live devices (.amxd patches)
- **Configurable landmark control** - fingers, palm, wrist positions, and more
- **GPU acceleration** with MediaPipe for smooth processing
- **Network flexibility** - local or remote OSC communication

## Getting Started

### Prerequisites
## System Requirements

To run this system, you will need the following software and hardware:

### Software
- **Python**: Python 3.13.0
- **MediaPipe**: Computer vision processing
- **Max/MSP**: Version 9.0.7 for patch processing
- **Ableton Live**: Version 12 integration
- **OSC (Open Sound Control)**: For communication between Python and Max/MSP

### Hardware
- **MacBook Air**: Apple M2 with 8 GB RAM

## Requirements

To run, you'll need the following Python libraries installed:
### Installation

Before running the system, make sure you have the necessary Python libraries installed. You can install them using **pip** by running the following commands:

```bash
pip install opencv-python
pip install mediapipe
pip install python-osc
  
```

### 1. Clone the Repository

To clone the repository to your local machine, open your terminal or command prompt and run the following command:

```bash
git clone https://github.com/JiaxiWang05/gesturecap_mapping.git

  
```




2. **Navigate to the Repository**

Once the repository is cloned, navigate into the project folder:
   ```bash
cd gesturecap_mapping
```
3. Run the Script

Once everything is set up, you can start the system by running the Python script.
   
```bash
python src/python/Realtime_Hand_Coordinate.py

```
This will launch the hand gesture control system, with your webcam tracking hand movements and sending OSC messages to control MAX Dials. 

5. Stopping the Program

To stop the program, simply press q when the OpenCV window is open, or close the terminal window or press Cmd + C on macOS to send an interrupt signal to the running process, which typically terminates the script.


 
