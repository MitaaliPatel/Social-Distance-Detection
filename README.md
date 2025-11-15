# **Social Distancing Detection using poseNet**

## **Overview**

This project demonstrates a simple real-time social-distancing detection system using **NVIDIA Jetson**, **poseNet**, and a USB camera.
The script detects people in the camera feed, computes distances between them based on pose keypoints, and alerts when two individuals are too close according to the defined threshold.

## **Features**

* Human pose detection using `resnet18-body`
* Real-time distance calculation between detected people
* Alerts printed in terminal when a violation occurs
* Visual overlay of pose keypoints and skeleton on the camera feed
* Designed for Jetson Nano / Xavier / Orin platforms

## **Hardware & Software Requirements**

### **Hardware**

* NVIDIA Jetson device
* USB camera connected at `/dev/video0`

### **Software**

* JetPack with:

  * jetson-inference
  * jetson.utils
* Python 3

## **How It Works**

1. poseNet detects human keypoints in each camera frame.
2. The script extracts the **left hip** and **right hip** positions for each person.
3. It computes the midpoint between hips as the "center" of each detected person.
4. The pairwise pixel distance between all centers is calculated.
5. If any distance is below the threshold, the script prints:

   ```
   Social Distancing Violation Detected!
   ```

## **Distance Threshold**

The threshold used is:

```
DIST_THRESHOLD = 150
```

This value represents **pixel distance**, not real physical units.
You may adjust this depending on your camera angle, field of view, and room size.

## **How to Run**

Make sure your Jetson is connected to a USB camera, then run:

```
python3 social_distance.py
```

You will see:

* A video window showing pose detection
* Terminal logs showing violation alerts when detected

## **Output Example**

Place this screenshot in your repository as:

<img width="1600" height="900" alt="image" src="https://github.com/user-attachments/assets/4f43794a-0ec4-446a-9a9d-b2be7b7761cb" />

## **Notes**

* The warnings such as
  `duplicate link detected, skipping...`
  `line has length < 2, skipping`
  are normal poseNet debug messages.
* This script does not save images; you may manually photograph your Jetson display for documentation.
