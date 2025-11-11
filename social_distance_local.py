import jetson.inference
import jetson.utils
import time

# Initialize poseNet
net = jetson.inference.poseNet("resnet18-body", threshold=0.15)

# Open camera feed
camera = jetson.utils.videoSource("/dev/video0", argv=['--input-width=640', '--input-height=480'])

# Display on Jetson screen
display = jetson.utils.videoOutput("display://0")

while display.IsStreaming() and camera.IsStreaming():
    img = camera.Capture()
    poses = net.Process(img)
    net.Render(img)
    net.PrintOutput()
    display.Render(img)
    time.sleep(0.01)
