# FEUP-AI - Partitions Game

## Description

This project is focused on the development of the **Partitions** game, a two-player adversarial board game that uses a hexagonal grid. The game allows for different board sizes and incorporates AI algorithms to enable a computer to play against either a human or another computer. The main goal of the project was to implement adversarial search algorithms, namely **Minimax with Alpha-Beta pruning** and **Monte Carlo Tree Search (MCTS)**, to enhance the decision-making capabilities of the AI players at various difficulty levels.

## Features

- **Game Modes**: 
  - Human vs Human
  - Human vs Computer
  - Computer vs Computer

- **AI Algorithms**:
  - **Minimax with Alpha-Beta Pruning** for medium and hard difficulty.
  - **Monte Carlo Tree Search (MCTS)** for medium and hard difficulty.

- **Difficulty Levels**:
  - Easy: Random moves.
  - Medium: Uses Minimax or MCTS with lower depth/simulations.
  - Hard: Uses Minimax or MCTS with more thinking time.

- **Hexagonal Board and GUI**: A fully interactive board is designed using Pygame with the capability of adjusting the size of the board.

- **Hint System**: Using Minimax, the system provides move suggestions for human players.

- **Logging & CSV Export**: All moves are logged and exported to a CSV file, including the time taken for each move, the player, and the game outcome.

## Requirements

- Python 3.x
- Pygame library
- NumPy library

## Installation

1. Download the project

2. Install required dependencies:

pip install pygame numpy

## Usage

1. Run the game by executing the `Partitions.py` file:

python Partitions.py

2. The game will prompt you to choose a game mode:
- Human vs Human
- Human vs Computer
- Computer vs Computer

3. If playing against AI, you will be asked to select the difficulty level and the AI algorithm to use (Minimax or MCTS).

4. Once the game ends, a CSV file will be generated with all the move logs and times taken for each move.

## AI Algorithms

### Minimax with Alpha-Beta Pruning

- The **Minimax** algorithm looks ahead at possible future moves and chooses the one that maximizes the player's chances of winning. 
- **Alpha-Beta Pruning** optimizes the Minimax search by eliminating branches of the search tree that do not need to be explored, saving computation time.

### Monte Carlo Tree Search (MCTS)

- MCTS simulates multiple random games (playouts) to explore different potential outcomes. 
- It evaluates moves by simulating a large number of possible future moves and selects the one with the highest success rate.

## Experimental Results

The following results show the time taken for different AI difficulty levels (Easy, Medium, Hard) using **Minimax** and **MCTS** algorithms.

- **Minimax (Easy & Medium)**: Faster decision-making but less optimized for deeper game trees.
- **MCTS (Hard)**: Slower, but can make better decisions after simulating many more random plays.

## Authors and Acknowledgments

- **Aléssia Jorge** - up202109242
- **Lara Cunha** - up202108876
- **Mo'men Alhammadin** - up202411533

## Related Work

- **Partitions Board Game**: [BoardGameGeek Partitions](https://boardgamegeek.com/boardgame/439137/partitions)
- **Minimax & Alpha-Beta Pruning**: Algorithms based on the teacher’s slides.
- **Monte Carlo Tree Search**: Based on game theory and decision-making techniques.
- **Pygame Documentation**: [Pygame Docs](https://www.pygame.org/docs/)

