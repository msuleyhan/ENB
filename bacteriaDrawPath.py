from opencv_browser_camera import BrowserCamera
import cv2
import numpy as np
import time
import math

# Initialize the browser camera
cap = BrowserCamera()
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 500)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 500)

# Setup SimpleBlobDetector parameters.
params = cv2.SimpleBlobDetector_Params()

# Change thresholds
params.minThreshold = 10
params.maxThreshold = 200

# Filter by Area.
params.filterByArea = True
params.minArea = 2  # Minimum area in pixels for detected blobs

# Filter by Circularity
params.filterByCircularity = True
params.minCircularity = 0.1

# Filter by Convexity
params.filterByConvexity = False

# Filter by Inertia
params.filterByInertia = True
params.minInertiaRatio = 0.01

# Create a detector with the parameters
detector = cv2.SimpleBlobDetector_create(params)

# Initialize variables to store initial keypoints and start time
initial_keypoints = None
start_time = time.time()
tracking_duration = 10  # Duration to finalize detection in seconds

# A dictionary to store bacteria positions for drawing paths
paths = {}

# Main loop
while True:
    print("loop")
    ret, frame = cap.read()

    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect blobs only during the first 10 seconds
    if time.time() - start_time <= tracking_duration:
        initial_keypoints = detector.detect(gray)
        # Reset paths for each detected bacteria
        paths = {kp.pt: [kp.pt] for kp in initial_keypoints}
    else:
        # Detect blobs continuously
        keypoints = detector.detect(gray)
        # Update paths for each bacteria
        for kp in keypoints:
            # Find the closest initial keypoint to continue the path
            closest_initial = min(initial_keypoints, key=lambda ikp: np.linalg.norm(np.array(kp.pt) - np.array(ikp.pt)))
            if np.linalg.norm(np.array(kp.pt) - np.array(closest_initial.pt)) < 50:  # threshold to consider same bacteria
                paths[closest_initial.pt].append(kp.pt)

    # Draw detected blobs and their paths
    im_with_keypoints = frame.copy()
    for initial_pt, path in paths.items():
        for i in range(1, len(path)):
            cv2.line(im_with_keypoints, tuple(int(x) for x in path[i - 1]), tuple(int(x) for x in path[i]), (0, 255, 0), 2)
        cv2.circle(im_with_keypoints, tuple(int(x) for x in initial_pt), 5, (0, 0, 255), -1)

    # Draw the number of initially detected bacteria
    cv2.putText(im_with_keypoints, f"Bacteria Count: {len(initial_keypoints)}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    # Display the frame with keypoints and bacteria count
    cv2.imshow("Bacteria Detection", im_with_keypoints)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
