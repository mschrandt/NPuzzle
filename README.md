# NPuzzle
Run `python play.py` to play the 15 Puzzle. You can modify the 'BOARD_SIZE' constant in `play.py` to 3 to play an 8 puzzle or 5 to play a 24 puzzle, etc.

## Controls
- **Left mouse click** to move a tile that is adjacent to the blank space
- **r** to shuffle the board
- **h** to run algorithm to find optimal solution. Continue hitting h to play next move. A pattern database is required to get a solution for a 15 puzzle or larger.

# Pattern Database
Run `python patternDb.py` to rebuild the pattern database file. By default, it will build a 663 partitioned pattern DB for a 15 puzzle on 2 threads. You can modify the board size, partitions, and number of parallel threads in the `patternDb.py main()` function. The pattern database file included in this git repo is a 555 partition for a 15 puzzle.
