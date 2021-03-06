# card_game_oop
A python based card game to get familiar with oop principles

## Description
This program is a basic card game to get us BeCoders familiar with the principles of oop

As a base this program runs a small card game with a deck of 52 cards being divided across 4 players and them playing a random card each turn untill their hands are empty. In main.py, as you can see below, the 4 players are created and added to a board, then this board starts the game. To add extra player one just needs to create an extra player and also add them to the board before the game is started.

```python
  5 amanda = Player("Amanda", [])
  6 jeff = Player("Jeff", [])
  7 nathan = Player("Nathan", [])
  8 berkley = Player("Berkley", [])
  9 
 10 game = Board([amanda, jeff, nathan, berkley])
 11 
 12 game.start_game()
```

## Installation

The program runs on python 3.8.10. As long as the `random` and `itertools` modules are present on your python installation, the code should run without issues.  

## Usage

To run the program, run the main.py file either by using the built in functionality in your editor or by simply running it with your python installation with `python path/to/main.py` (or `python path\to\main.py`). Depending on your installation you may need to use `python3` rather than `python`.
