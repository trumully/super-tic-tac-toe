# Super Tic-tac-toe

I saw the game in Vsauce's [How to Play Super Tic-Tac-Toe](https://www.youtube.com/watch?v=_Na3a1ZrX7c) and wanted to reproduce it, so here it is! A mock-up of it made in Python

```shell
- - - | - - - | - - -
- - - | - - - | - o -
- - - | - - - | - - -
---------------------
- - - | - - x | - - -
- - - | - x - | - - -
- - - | - - - | - - -
---------------------
- - - | - - - | - - -
- - - | - - - | - - -
- - - | - - - | - - -

o | choose a square to play in (x, y): 0, 2
- - - | - - - | - - -
- - - | - - - | - o -
- - - | - - - | - - -
---------------------
- - - | - - x | - - -
- - - | - x - | - - -
- - - | o - - | - - -
---------------------
- - - | - - - | - - -
- - - | - - - | - - -
- - - | - - - | - - -
```

## How it's played
- The starting player can choose any grid to start in.
- They then pick a square in the chosen grid to play.
- The next player must then **play a move in that corresponding grid.**
- Repeat until someone has a line of winning games.
- If a singular grid ends as a draw, that grid is forfeitted.
- If the entire game draws then the winner is the one with the most total grids won.