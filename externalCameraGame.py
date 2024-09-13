import cv2
import numpy as np
import time
import random

# Initialize the camera
cap = cv2.VideoCapture(1)  # Use 0 for default camera, 1 for external, etc.

# Check if the camera opened successfully
if not cap.isOpened():
    print("Error: Camera could not be opened.")
    exit()

# Set camera resolution
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 500)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 500)

# Setup SimpleBlobDetector parameters.
params = cv2.SimpleBlobDetector_Params()
params.minThreshold = 10
params.maxThreshold = 200
params.filterByArea = True
params.minArea = 2
params.filterByCircularity = True
params.minCircularity = 0.1
params.filterByConvexity = False
params.filterByInertia = True
params.minInertiaRatio = 0.01

detector = cv2.SimpleBlobDetector_create(params)

# Timing and states
initial_detection_time = 10  # seconds
game_duration = 60  # seconds
result_display_duration = 10  # seconds
start_time = time.time()
last_state_change = time.time()

initial_keypoints = []
paths = {}
game_state = 'detecting'  # Can be 'detecting', 'tracking', 'show_result'
target_region = None
region_count = 0

def is_in_target_region(point, region, width, height):
    x, y = point
    if region == 'top':
        return y < height / 2
    elif region == 'bottom':
        return y >= height / 2
    elif region == 'left':
        return x < width / 2
    elif region == 'right':
        return x >= width / 2

def highlight_region(frame, region, width, height):
    overlay = frame.copy()
    alpha = 0.3  # Transparency factor.

    if region == 'top':
        cv2.rectangle(overlay, (0, 0), (width, height // 2), (255, 255, 0), -1)  # Yellow
    elif region == 'bottom':
        cv2.rectangle(overlay, (0, height // 2), (width, height), (255, 255, 0), -1)  # Yellow
    elif region == 'left':
        cv2.rectangle(overlay, (0, 0), (width // 2, height), (255, 255, 0), -1)  # Yellow
    elif region == 'right':
        cv2.rectangle(overlay, (width // 2, 0), (width, height), (255, 255, 0), -1)  # Yellow

    cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)

# Main loop
while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    current_time = time.time()
    elapsed_time = current_time - start_time

    # Game state management
    if game_state == 'detecting' and elapsed_time <= initial_detection_time:
        keypoints = detector.detect(gray)
        initial_keypoints = keypoints
        paths = {kp.pt: [kp.pt] for kp in keypoints}
        print(f"Detecting... {len(keypoints)} bacteria detected.")
    elif game_state == 'detecting' and elapsed_time > initial_detection_time:
        game_state = 'tracking'
        last_state_change = current_time
        target_region = random.choice(['top', 'bottom', 'left', 'right'])
        print(f"Tracking in region: {target_region}")
    elif game_state == 'tracking' and current_time - last_state_change > game_duration:
        game_state = 'show_result'
        last_state_change = current_time
        region_count = sum(1 for path in paths.values() if is_in_target_region(path[-1], target_region, 500, 500))
        print(f"Bacteria in {target_region}: {region_count}")
    elif game_state == 'show_result' and current_time - last_state_change > result_display_duration:
        game_state = 'tracking'
        last_state_change = current_time
        target_region = random.choice(['top', 'bottom', 'left', 'right'])
        paths = {kp.pt: [kp.pt] for kp in initial_keypoints}  # Reset paths
        print(f"New round: Tracking in region: {target_region}")

    # Update paths if tracking
    if game_state == 'tracking':
        keypoints = detector.detect(gray)
        for kp in keypoints:
            closest_initial = min(initial_keypoints, key=lambda ikp: np.linalg.norm(np.array(kp.pt) - np.array(ikp.pt)))
            if np.linalg.norm(np.array(kp.pt) - np.array(closest_initial.pt)) < 50:
                paths[closest_initial.pt].append(kp.pt)

    # Highlight region if tracking
    if game_state == 'tracking':
        highlight_region(frame, target_region, 500, 500)

    # Draw paths and keypoints
    for initial_pt, path in paths.items():
        for i in range(1, len(path)):
            cv2.line(frame, tuple(int(x) for x in path[i - 1]), tuple(int(x) for x in path[i]), (0, 255, 0), 2)
        cv2.circle(frame, tuple(int(x) for x in initial_pt), 5, (0, 0, 255), -1)

    # Display text based on state
    if game_state == 'tracking':
        cv2.putText(frame, f"Time left: {int(game_duration - (current_time - last_state_change))}s", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
    elif game_state == 'show_result':
        cv2.putText(frame, f"Bacteria in {target_region}: {region_count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

    # Show the image
    cv2.imshow('Bacteria Tracking Game', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Clean up
cap.release()
cv2.destroyAllWindows()
