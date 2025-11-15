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

# pixel distance threshold for violation (tune as needed)
DIST_THRESHOLD = 150

while display.IsStreaming():
    # capture frame (with timeout)
    img = camera.Capture(timeout=5000)
    if img is None:
        print("No image captured, skipping frame...")
        continue

    # process image for pose estimation
    poses = net.Process(img, overlay="links,keypoints")

    # store midpoints between hips for each person
    centers = []
    for p in poses:
        try:
            left_hip = p.Keypoints[11]
            right_hip = p.Keypoints[12]
            cx = (left_hip.x + right_hip.x) / 2
            cy = (left_hip.y + right_hip.y) / 2
            centers.append((cx, cy))
        except:
            pass  # skip if hips not detected

    # check distances between each pair of people
    violation = False
    for i in range(len(centers)):
        for j in range(i + 1, len(centers)):
            dist = math.hypot(centers[i][0] - centers[j][0],
                              centers[i][1] - centers[j][1])
            if dist < DIST_THRESHOLD:
                violation = True

    # print alert if violation found
    if violation:
        print("Social Distancing Violation Detected!")

    # render output frame
    display.Render(img)
    display.SetStatus("Social Distancing Detection | {:.0f} FPS".format(net.GetNetworkFPS()))
