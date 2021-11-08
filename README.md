# Privilege-Recognition-Task

## Game Directions
1. Answer the questionaire with the mouse and submit when done
2. Use arrow keys or WASD to move (you are player 1)
3. Collect as many coins as possible


## How to run
Requirements:

- pygame
- python3

## Option 1: Downloading the exe
1. Download the executable from either the mac or windows folder
2. Run it and follow the directions

### Updating the Game
1. Redownload it from the repo



## Option 2: Cloning the repo
### Instructions:
1. Download the Privilege task repo
2. Navigate the command line to the directory PAT
3. Call `python3 ../PAT/`
4. enter a number for a seed
5. enter a name for the config directory (like "test") 
7. You will enter a full screen
8. play the game
9. press esc to exit the game

### Updating the game
1. Navigate the command line to the github directory
2. Call 'git pull'


## Features:
- 1 player vs 3 AI
- Multiple Rounds
- Record every input from the player (time-stamped by by game tick)
- Player moves up, down, left, right. Collect coins
- Experiment parameters: Coin distrobution, speed, number of rounds
- AI either has optimal, random, or "stay still" movement (random walk via markov chain)
- Feedback: Number of Coins per player/enemy
- Configuration for each "level"
- Gradient Setting for bias
- Single choice questions
- Multiple choice questions
- slider questions
- JSON configuration file
- Modular ordering of configurations
