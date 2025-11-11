## Social Distance Detection using Jetson PoseNet

This project uses NVIDIA Jetson's `poseNet` model to detect human poses and estimate the distance between people in a live video feed. If individuals are detected to be too close to one another, the system can flag them as being in violation of social distancing norms.

## Features
- Real-time human pose detection using `poseNet`
- Distance estimation between detected people
- Visual display of the live camera feed with pose skeletons
- Runs directly on NVIDIA Jetson devices (tested on Jetson Orin Nano)

## Requirements
Before running this project, ensure your Jetson device has the following installed:
- JetPack SDK (with CUDA, TensorRT, and OpenCV)
- `jetson-inference` and `jetson-utils` libraries
- Python 3
- USB camera or CSI camera connected to the Jetson

## Setup
1. Clone or copy this repository to your Jetson device:
   ```bash
   git clone https://github.com/<your-username>/social-distance-detection.git
   cd social-distance-detection

Make sure the following files are present:

1. social_distance_local.py

2. posenet.py

   Run the project locally on your Jetson display:
   ```bash
   python3 social_distance_local.py

## Output

A live camera window will appear showing the detected human poses.
Each person is outlined with a skeleton, and the script can calculate spacing to determine if social distancing is being maintained.


## This project was developed as part of a Jetson lab assignment.

## For any setup issues, ensure your camera is not already in use by another application.
