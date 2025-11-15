# **Social Distancing Detection using poseNet**

## **Overview**

This project demonstrates a simple real-time social-distancing detection system using **NVIDIA Jetson**, **poseNet**, and a USB camera.
The script detects people in the camera feed, computes distances between them based on pose keypoints, and alerts when two individuals are too close according to the defined threshold.

---

## **Features**

* Human pose detection using `resnet18-body`
* Real-time distance calculation between detected people
* Alerts printed in terminal when a violation occurs
* Visual overlay of pose keypoints and skeleton on the camera feed
* Designed for Jetson Nano / Xavier / Orin platforms

---

## **Hardware & Software Requirements**

### **Hardware**

* NVIDIA Jetson device
* USB camera connected at `/dev/video0`

### **Software**

* JetPack with:

  * jetson-inference
  * jetson.utils
* Python 3

---

## **How It Works**

1. poseNet detects human keypoints in each camera frame.
2. The script extracts the **left hip** and **right hip** positions for each person.
3. It computes the midpoint between hips as the "center" of each detected person.
4. The pairwise pixel distance between all centers is calculated.
5. If any distance is below the threshold, the script prints:

   ```
   Social Distancing Violation Detected!
   ```

---

## **Distance Threshold**

The threshold used is:

```
DIST_THRESHOLD = 150
```

This value represents **pixel distance**, not real physical units.
You may adjust this depending on your camera angle, field of view, and room size.

---

## **How to Run**

Make sure your Jetson is connected to a USB camera, then run:

```
python3 social_distance.py
```

You will see:

* A video window showing pose detection
* Terminal logs showing violation alerts when detected

---

## **Output Example**

Place this screenshot in your repository as:

```
/images/violation_output.jpeg
```

Then reference it like this:

```
![Social Distancing Detection Output](images/violation_output.jpeg)
```

---

## **Code**

```python
# Simple Social Distancing Detection using poseNet

import jetson.inference
import jetson.utils
import math
import time

# load poseNet model
net = jetson.inference.poseNet("resnet18-body", threshold=0.15)

# open camera stream (use MJPEG mode)
camera = jetson.utils.videoSource("v4l2:///dev/video0", [
    "--input-width=640",
    "--input-height=480",
    "--input-codec=mjpeg"
])

# open display window
display = jetson.utils.videoOutput("display://0")

# allow camera to warm up
time.sleep(2)

# pixel distance threshold for violation
DIST_THRESHOLD = 150

while display.IsStreaming():
    img = camera.Capture(timeout=5000)
    if img is None:
        print("No image captured, skipping frame...")
        continue

    poses = net.Process(img, overlay="links,keypoints")

    centers = []
    for p in poses:
        try:
            left_hip = p.Keypoints[11]
            right_hip = p.Keypoints[12]
            cx = (left_hip.x + right_hip.x) / 2
            cy = (left_hip.y + right_hip.y) / 2
            centers.append((cx, cy))
        except:
            pass

    violation = False
    for i in range(len(centers)):
        for j in range(i + 1, len(centers)):
            dist = math.hypot(centers[i][0] - centers[j][0],
                              centers[i][1] - centers[j][1])
            if dist < DIST_THRESHOLD:
                violation = True

    if violation:
        print("Social Distancing Violation Detected!")

    display.Render(img)
    display.SetStatus("Social Distancing Detection | {:.0f} FPS".format(net.GetNetworkFPS()))
```

---

## **Notes**

* The warnings such as
  `duplicate link detected, skipping...`
  `line has length < 2, skipping`
  are normal poseNet debug messages.
* This script does not save images; you may manually photograph your Jetson display for documentation.

Just tell me.
