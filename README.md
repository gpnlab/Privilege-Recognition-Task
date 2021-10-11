# Privilege-Recognition-Task
## How to run
Requirements:

- pygame
- python3

## Updating the game
1. Navigate the command line to the github directory
2. Call 'git pull'

Instructions:
1. Download the Privilege task repo
2. Navigate the command line to the directory PAT
3. Call `python3 ../PAT/`
4. enter a number for a seed
5. enter a name for the config directory (like "test") 
7. You will enter a full screen
8. play the game
9. press esc to exit the game

## 09/20 Week Tasks:

1. Improve the ai to be more 'human'

    a. Lit. review
  
  
    b. Implementation
  
  
2. Fix the EXE pathing when writing logs

## Completed:

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
- JSON configuration file
