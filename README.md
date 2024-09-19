# ENB: Euglena's Not a Bacteria Project

## Team Members:
- Suleyman Hanyyev
- Anja Stijepovic
- Maria Petropoulos
- Leo Villemin

## TLDR;
ENB is a simple biotic game that detects 50 euglenas and tracks their path. The challenge is to move euglenas to a randomly selected block of the screen:
Top/Bottom/Left/Right.
User is given a minute to move the euglenas to the correct block.
Then the game will show the number of the euglenas that passed to the block.
After that round, the game waits for 10 seconds and resets.
The most important thing: You try to move the euglenas with the LED light that is controlled by the joystick

## How to play the game
- Connect the joystick to the arduino
- Connect the arduino to the computer
- Run the code
- You will see the euglenas detected by the camera
- The game will randomly select a block (Top/Bottom/Left/Right)
- That Block will be shown on the screen (highlighted)
- Move the joystick to move the LED light
- Wait till the euglenas move to the correct block (or pray, whatever works)
- The game will show the number of euglenas that passed to the correct block
- The game will wait for 10 seconds and reset

## Additional
While writing the code for this game, we also created some learning tools and games alongside.
- We created a simple game that detects the number of euglenas in the screen.
- We created a simple game that detects the number of euglenas in the screen and tracks their path.
- We created a simple python script that detects your face and just puts a rectangle on it
- We created a ping pong game, where the user can play against the computer
- We created a ping pong game, where the user can play against the user
- We created a ping pong game, where the computer can play against the computer. It is called "What's the point of the bacteria?"

## Folder Structure
./
 - euglenamaingame.py
 - games/
    - bacteria.py
 - learning/
    - rectangleAroundFace.py
 - arduino/
 - pictures/
 - videos/

## Important Components
- Joystick
- Arduino
- LED lights
- Code for Arduino (in this repo)
- Code for the game (in this repo)
- The holder that holds the phone on top of the microscope [here's the link](https://www.thingiverse.com/thing:3384088)
