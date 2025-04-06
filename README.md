# Connect Four Game

A Python implementation of the classic Connect Four game with an interactive GUI and AI opponents of varying difficulty levels.

## Overview

This project provides a complete Connect Four game with a graphical user interface built using Pygame. Players can compete against different AI opponents with varying levels of difficulty:

- **Easy**: Uses random move selection
- **Medium**: Uses the Minimax algorithm with limited depth
- **Hard**: Uses an improved Minimax algorithm with alpha-beta pruning and better position evaluation

## Files

The project consists of three main Python files:

1. `connect_four_game.py`: Contains the core game logic and rules
2. `connect_four_ai.py`: Implements the AI opponents (RandomAgent, MinimaxAgent, ImprovedMinimaxAgent)
3. `connect_four_gui.py`: Provides the graphical user interface using Pygame

## Requirements

- Python 3.x
- Pygame
- NumPy

## Installation

1. Clone or download this repository
2. Install the required dependencies:

```bash
pip install pygame numpy
```

## How to Play

1. Run the game:

```bash
python connect_four_gui.py
```

2. From the main menu, select the difficulty level of the AI opponent
3. Click on a column to drop your piece (red)
4. The AI (yellow) will automatically make its move
5. The first player to connect four pieces horizontally, vertically, or diagonally wins
6. After the game ends, click "Play Again" to return to the main menu

## Game Features

- Interactive GUI with visual feedback
- Piece-dropping animations
- Three difficulty levels of AI opponents
- Game state tracking (wins, draws)
- Play again functionality

## AI Implementation

### RandomAgent
- Makes random moves from the set of valid columns

### MinimaxAgent
- Uses the Minimax algorithm to search for optimal moves
- Limited search depth to maintain reasonable performance
- Basic position evaluation

### ImprovedMinimaxAgent
- Extends MinimaxAgent with alpha-beta pruning for more efficient search
- Enhanced position evaluation that considers potential winning sequences
- Can look ahead more moves due to improved search efficiency

## Future Improvements
- Potential enhancements for future versions:
- Player vs. Player mode
- Score tracking across multiple games
- Customizable board sizes
- Sound effects and music
- More sophisticated AI strategies

## License
This project is open source and available for educational and personal use.

## Acknowledgements
This project was created as an educational exercise in game development, AI algorithms, and GUI programming with Python.
