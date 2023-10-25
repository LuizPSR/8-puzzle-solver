# 8-puzzle-solver
A 8-Puzzle solver implemented in python using multiple algorithms

## Usage
python 8-puzzle.py \<algorithm> \<initial state> \<'' or print>

### Algorithms Implemented
- **B**: Breadth First Search
- **I**: Iterative Deepening Search
- **U**: Uniform Cost Search
- **A**: A* Algorithm Search
- **G**: Greedy Best First Search
- **H**: Hill Climbing

### Initial State
|1|2|3|
|---|---|---|
|**4**|**5**|**6**|
|**7**|**8**||

is written as 1 2 3 4 5 6 7 8 0

### Print
By default only the number of moviments in the found solution is printed, but if print is passed as the last argument each move towards it will be printed
