# ENB: Euglena's Not a Bacteria Project

## Team Members:
- Suleyman Hanyyev
- Anja Stijepovic
- Maria Petropoulos
- Leo Villemin

## TLDR;
ENB is a simple biotic game that detects 50 euglenas and tracks their path. The challenge is to move euglenas to a randomly selected zone on the screen:
Top/Bottom/Left/Right.
User is given 30 seconds to move the euglenas to the correct zone.
Then the game will show the number of the euglenas that moved to that zone.
After that round, the game waits for 10 seconds and resets to have in total 3 rounds with three different zones.
The most important thing: Trying to move the euglenas with the LED light that is controlled by the joystick

## How to play the game
- Connect the joystick to the arduino
- Connect the arduino to the computer
- Set up the box with the LED lights as well as the euglena on the microscope
- Run the code
- You will see the euglenas detected by the camera
- The game will randomly select a zone (Top/Bottom/Left/Right)
- That zone will be shown on the screen (highlighted)
- Move the joystick to move the LED light
- Wait till the euglenas move to the correct zone (or pray, whatever works)
- The game will show the number of euglenas that passed to the correct block
- The game will wait for 10 seconds and reset to a new zone
- When the 3 rounds are done, a "Goodbye, game over" message will appear with the total amount of points

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
- Euglena
- Joystick
- Arduino
- LED lights
- Code for Arduino (in this repo)
- Code for the game (in this repo)
- The holder that holds the phone on top of the microscope [here's the link](https://www.thingiverse.com/thing:3384088)
- A case for the euglena and LED lights (to minimize outside light)
