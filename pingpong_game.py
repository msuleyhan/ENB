import cv2
import numpy as np
from opencv_browser_camera import BrowserCamera

# Initialize the browser camera
cap = BrowserCamera()
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 500)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 700)
cap.set(cv2.CAP_PROP_FPS, 20)

# Define initial positions and settings
def reset_ball():
    return 250, 350, 5 * np.random.choice([-1, 1]), 5 * np.random.choice([-1, 1])

# Game variables
paddle1_x, paddle1_y = 250, 650  # Bottom paddle
paddle2_x, paddle2_y = 250, 50   # Top paddle
ball_x, ball_y, velocity_x, velocity_y = reset_ball()
ball_radius = 10
paddle_width, paddle_height = 100, 10
score_player1, score_player2 = 0, 0  # Score tracking

while True:
    ret, frame = cap.read()

    frame = cv2.flip(frame, 1)  # Flip the frame horizontally
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # Convert to HSV color space

    # This part is for example, adjust according to how you'll track two different objects
    # Define the color range for paddle detection (e.g., blue and red objects)
    lower_blue = np.array([100, 150, 50])
    upper_blue = np.array([140, 255, 255])
    lower_red = np.array([0, 120, 70])
    upper_red = np.array([10, 255, 255])

    # Threshold the HSV image to get colors
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
    mask_red = cv2.inRange(hsv, lower_red, upper_red)

    # Find contours for blue (player 1)
    contours_blue, _ = cv2.findContours(mask_blue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours_blue:
        largest_contour_blue = max(contours_blue, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour_blue)
        paddle1_x = x + w // 2

    # Find contours for red (player 2)
    contours_red, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours_red:
        largest_contour_red = max(contours_red, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour_red)
        paddle2_x = x + w // 2

    # Ball movement logic
    ball_x += velocity_x
    ball_y += velocity_y

    # Boundary checking
    if ball_x < ball_radius or ball_x > 500 - ball_radius:
        velocity_x *= -1
    if ball_y < ball_radius + paddle_height and paddle2_x - paddle_width // 2 < ball_x < paddle2_x + paddle_width // 2:
        velocity_y *= -1
    elif ball_y > 650 - ball_radius - paddle_height and paddle1_x - paddle_width // 2 < ball_x < paddle1_x + paddle_width // 2:
        velocity_y *= -1
    elif ball_y < 0:  # Player 1 scores
        score_player1 += 1
        ball_x, ball_y, velocity_x, velocity_y = reset_ball()
    elif ball_y > 700:  # Player 2 scores
        score_player2 += 1
        ball_x, ball_y, velocity_x, velocity_y = reset_ball()

    # Drawing the paddles and the ball
    cv2.rectangle(frame, (paddle1_x - paddle_width // 2, 650), (paddle1_x + paddle_width // 2, 660), (255, 255, 255), -1)
    cv2.rectangle(frame, (paddle2_x - paddle_width // 2, 50), (paddle2_x + paddle_width // 2, 60), (255, 255, 255), -1)
    cv2.circle(frame, (ball_x, ball_y), ball_radius, (0, 255, 255), -1)

    # Display scores
    cv2.putText(frame, f"Player 1: {score_player1}", (10, 675), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    cv2.putText(frame, f"Player 2: {score_player2}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    # Display the resulting frame
    cv2.imshow("Ping Pong", frame)
    cv2.waitKey(1)
