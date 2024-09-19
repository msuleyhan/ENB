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
paddle1_x, paddle1_y = 250, 650  # Bottom paddle (NPC 1)
paddle2_x, paddle2_y = 250, 50   # Top paddle (NPC 2)
ball_x, ball_y, velocity_x, velocity_y = reset_ball()
ball_radius = 10
paddle_width, paddle_height = 100, 10
score_npc1, score_npc2 = 0, 0  # Score tracking

# Main game loop
while True:
    ret, frame = cap.read()

    frame = cv2.flip(frame, 1)  # Flip the frame horizontally
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # Convert to HSV color space

    # Move paddles (NPC logic: follow the ball)
    if ball_x > paddle1_x:
        paddle1_x += 5  # NPC 1 moves right
    elif ball_x < paddle1_x:
        paddle1_x -= 5  # NPC 1 moves left

    if ball_x > paddle2_x:
        paddle2_x += 5  # NPC 2 moves right
    elif ball_x < paddle2_x:
        paddle2_x -= 5  # NPC 2 moves left

    # Ball movement logic
    ball_x += velocity_x
    ball_y += velocity_y

    # Boundary checking and collision with paddles
    if ball_x < ball_radius or ball_x > 500 - ball_radius:
        velocity_x *= -1
    if ball_y < ball_radius + paddle_height and paddle2_x - paddle_width // 2 < ball_x < paddle2_x + paddle_width // 2:
        velocity_y *= -1
    elif ball_y > 650 - ball_radius - paddle_height and paddle1_x - paddle_width // 2 < ball_x < paddle1_x + paddle_width // 2:
        velocity_y *= -1
    elif ball_y < 0:  # NPC 1 scores
        score_npc1 += 1
        ball_x, ball_y, velocity_x, velocity_y = reset_ball()
    elif ball_y > 700:  # NPC 2 scores
        score_npc2 += 1
        ball_x, ball_y, velocity_x, velocity_y = reset_ball()

    # Drawing the paddles, ball, and title
    cv2.rectangle(frame, (paddle1_x - paddle_width // 2, 650), (paddle1_x + paddle_width // 2, 660), (255, 255, 255), -1)
    cv2.rectangle(frame, (paddle2_x - paddle_width // 2, 50), (paddle2_x + paddle_width // 2, 60), (255, 255, 255), -1)
    cv2.circle(frame, (ball_x, ball_y), ball_radius, (0, 255, 255), -1)

    # Display scores
    cv2.putText(frame, f"NPC 1: {score_npc1}", (10, 675), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    cv2.putText(frame, f"NPC 2: {score_npc2}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    # Add title in two lines to fit
    cv2.putText(frame, "What's the point of", (50, 330), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    cv2.putText(frame, "the bacteria?", (150, 360), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    # Display the resulting frame
    cv2.imshow("Ping Pong", frame)
    cv2.waitKey(1)
