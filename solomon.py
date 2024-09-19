from opencv_browser_camera import BrowserCamera
import cv2
import numpy as np
import time
import random

# Initialize the browser camera
cap = cv2.VideoCapture(0)
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
game_duration = 30  # seconds per zone
result_display_duration = 10  # seconds to display results
total_game_duration = 90  # Total game duration (for 3 zones)
start_time = time.time()
last_state_change = time.time()

initial_keypoints = []
paths = {}
game_state = 'detecting'  # Can be 'detecting', 'tracking', 'show_result', 'game_over'
target_region = None
region_count = 0
completed_zones = 0
region_counts = []  # To store the count of Euglena in each zone

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
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    current_time = time.time()
    elapsed_time = current_time - start_time

    # Game state management
    if game_state == 'detecting' and elapsed_time <= initial_detection_time:
        keypoints = detector.detect(gray)
        initial_keypoints = keypoints
        paths = {kp.pt: [kp.pt] for kp in keypoints}
        print(f"Detecting... {len(keypoints)} euglena detected.")
    
    elif game_state == 'detecting' and elapsed_time > initial_detection_time:
        total_euglena_text = f"Total detected: {len(initial_keypoints)}"
        (text_width, text_height), _ = cv2.getTextSize(total_euglena_text, cv2.FONT_HERSHEY_SIMPLEX, 1.0, 2)
        text_x = (frame.shape[1] - text_width) // 2
        text_y = (frame.shape[0] + text_height) // 2

        cv2.putText(frame, total_euglena_text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0), 2)
        
        if current_time - last_state_change > 10:  
            game_state = 'tracking'
            last_state_change = current_time
            target_region = random.choice(['top', 'bottom', 'left', 'right'])
            print(f"Tracking in region: {target_region}")
    
    elif game_state == 'tracking' and current_time - last_state_change > game_duration:
        game_state = 'show_result'
        last_state_change = current_time
        region_count = sum(1 for path in paths.values() if is_in_target_region(path[-1], target_region, 500, 500))
        print(f"Euglena in the {target_region} zone: {region_count}")
        region_counts.append(region_count)
        completed_zones += 1
    
    elif game_state == 'show_result' and current_time - last_state_change > result_display_duration:
        if completed_zones >= 3:
            game_state = 'game_over'
            total_score = sum(region_counts)  # Calculate the total score
        else:
            game_state = 'tracking'
            last_state_change = current_time
            target_region = random.choice(['top', 'bottom', 'left', 'right'])
            paths = {kp.pt: [kp.pt] for kp in initial_keypoints}  # Reset paths
            print(f"New round: Tracking in region: {target_region}")
    
    elif game_state == 'game_over':
        game_over_text = "GAME OVER"
        score_text = f"Your score: {sum(region_counts)}"
        
        (game_over_width, game_over_height), _ = cv2.getTextSize(game_over_text, cv2.FONT_HERSHEY_SIMPLEX, 1.5, 2)
        (score_width, score_height), _ = cv2.getTextSize(score_text, cv2.FONT_HERSHEY_SIMPLEX, 1.0, 2)
        
        game_over_x = (frame.shape[1] - game_over_width) // 2
        game_over_y = (frame.shape[0] // 2) - 40
        score_x = (frame.shape[1] - score_width) // 2
        score_y = game_over_y + game_over_height + 60
        
        # Draw the text without background
        cv2.putText(frame, game_over_text, (game_over_x, game_over_y), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 2)
        cv2.putText(frame, score_text, (score_x, score_y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0), 2)
    
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
        cv2.putText(frame, f"Euglena in the {target_region} zone: {region_count}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

    # Show the image
    cv2.imshow('ENB', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Clean up
cap.release()
cv2.destroyAllWindows()
