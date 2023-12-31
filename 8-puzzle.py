# -*- coding: utf-8 -*-
"""TP1 AI.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1qX6qdsrPAhNR_-ChegPi2YthnWq0sW5z
"""

import copy
import heapq
import random
import sys

GOAL = [[1,2,3],
        [4,5,6],
        [7,8,0]]

class Node:
  def __init__(self, state, parent=None, action=None, depth=0):
    self.state = copy.deepcopy(state)
    self.parent = parent
    self.action = action
    self.depth = depth

  def __lt__(self, other):
    return self.depth < other.depth

  def _find_zero(self):
    for i in range(3):
      for j in range(3):
        if self.state[i][j] == 0:
          return (i, j)

  def is_goal(self):
    if self.state == GOAL:
      return True
    return False

  def print_path(self):
    if self.parent is not None:
      self.parent.print_path()
    for i in range(3):
      for j in range(3):
        if self.state[i][j] != 0:
          print(self.state[i][j], end=' ')
        else:
          print(' ', end=' ')
      print()
    print()

  def expand(self):
    children = []
    row, col = self._find_zero()

    # for each possible action
    for dr, dc, move in [(0, 1, 'right'),
                         (1, 0, 'down'),
                         (0, -1, 'left'),
                         (-1, 0, 'up')]:

      r, c = row + dr, col + dc
      # if action is valid, add node as child
      if 0 <= r < 3 and 0 <= c < 3:
        new_state = copy.deepcopy(self.state)
        new_state[row][col] = new_state[r][c]
        new_state[r][c] = 0

        children.append(Node(new_state, self, move, self.depth + 1))

    return children

"""# Search Without Information

### Breadth First Search
"""

def BFS(state):
  explored = []
  frontier = [Node(state)]

  #expanded = 0
  #max_len = 1

  while frontier:
    node = frontier.pop(0)

    if node.is_goal():
      # a solution was found
      return node #, expanded, max_len

    # check if state was explored before expanding
    if node.state in explored:
      continue
    explored.append(node.state)

    # add unexplored children to frontier
    children = node.expand()
    for child in children:
      if child.state not in explored:
        frontier.append(child)

    #expanded += 1
    #max_len = max(max_len, len(frontier), len(explored))

  # no solution was found
  return None #, expanded, max_len

"""### Iterative Deepening Search"""

def IDS(state):

  #expanded = 0
  #max_len = 1

  for max_depth in range(40):
    frontier = [Node(state)]
    while frontier:
      node = frontier.pop(-1)
      if node.is_goal():
        # a solution was found
        return node #, expanded, max_len

      # add children to frontier, if not at max depth
      if node.depth >= max_depth:
        continue
      children = node.expand()
      for child in children:
        frontier.append(child)

      #expanded += 1
      #max_len = max(max_len, len(frontier))

  # no solution was found
  return None #, expanded, max_len

"""### Uniform Cost Search - Dijkstra"""

# OBS: since every action has cost 1, there is no difference in the execution
# of BFS and UCS

def UCS(state):
  explored = []
  frontier = []
  heapq.heappush(frontier, (0, Node(state)))

  #expanded = 0
  #max_len = 1

  while frontier:
    cost, node = heapq.heappop(frontier)
    if node.is_goal():
      # a solution was found
      return node #, expanded, max_len

    # check if state was explored before expanding
    if node.state in explored:
      continue
    explored.append(node.state)

    # add unexplored children to frontier
    children = node.expand()
    for child in children:
      if child.state not in explored:
        heapq.heappush(frontier, (child.depth, child))

    #expanded += 1
    #max_len = max(max_len, len(frontier), len(explored))

  # no solution was found
  return None #, expanded, max_len

"""# Search With Information

### Heuristic Functions
"""

def h1(state):
  distance = 0
  for i in range(3):
    for j in range(3):
      if (state[i][j] != GOAL[i][j] and
          state[i][j] != 3*i + j + 1):
        distance += 1
  return distance

def h2(state):
  distance = 0
  for i in range(3):
    for j in range(3):
      if state[i][j] != 0:
        r, c = divmod(state[i][j] - 1, 3)
        distance += abs(i - r) + abs(j - c)
  return distance

"""### A* Search"""

def AS(state):
  explored = []
  frontier = []
  heapq.heappush(frontier, (h2(state), Node(state)))

  #expanded = 0
  #max_len = 1

  while frontier:
    cost, node = heapq.heappop(frontier)
    if node.is_goal():
      # a solution was found
      return node #, expanded, max_len

    # check if state was explored before expanding
    if node.state in explored:
      continue
    explored.append(node.state)

    # add unexplored children to frontier
    children = node.expand()
    for child in children:
      if child.state not in explored:
        heapq.heappush(frontier, (h2(child.state) + child.depth, child))

    #expanded += 1
    #max_len = max(max_len, len(frontier), len(explored))

  # no solution was found
  return None #, expanded, max_len

"""### Greedy Best First Search"""

def GBFS(state):
  explored = []
  frontier = []
  heapq.heappush(frontier, (h2(state), Node(state)))

  #expanded = 0
  #max_len = 1

  while frontier:
    cost, node = heapq.heappop(frontier)
    if node.is_goal():
      # a solution was found
      return node #, expanded, max_len

    # check if state was explored before expanding
    if node.state in explored:
      continue
    explored.append(node.state)

    # add unexplored children to frontier
    children = node.expand()
    for child in children:
      if child.state not in explored:
        heapq.heappush(frontier, (h2(child.state), child))

    #expanded += 1
    #max_len = max(max_len, len(frontier), len(explored))

  # no solution was found
  return None #, expanded, max_len

"""
# Local Search

### Hill Climbing"""

def HC(state):
  node = Node(state)
  curr_cost = h2(node.state)

  #expanded = 0

  # never undo the last step to avoid loops
  last_state = None

  K = 5
  k = 0
  # if K consecutive steps without improvement, give up
  while k <= K:
    if node.is_goal():
      # a solution was found
      return node #, expanded

    # expand node to find best child
    children = node.expand()

    # suffle to prevent the predetermined pattern of moves
    # to create loops
    random.shuffle(children)

    # find steepest ascend
    best_child = None
    cost = float("inf")
    for child in children:
      child_cost = h2(child.state)
      if child_cost < cost and child.state != last_state:
        best_child = child
        cost = child_cost

    # if lateral step, updade counter
    if cost >= curr_cost:
      k += 1
    else:
      k = 0

    last_state = node.state
    node = best_child
    curr_cost = cost

    #expanded += 1

  # no solution was found
  return None #, expanded

"""# Main Execution"""

# test case
#args = ['A','0','8','7','5','4','2','1','6','3','print']

args = sys.argv[1:]
assert len(args) > 9, "not enought arguments"

# get solver algorithm
solver = None
for char, f in [('B', BFS ),
                ('I', IDS ),
                ('U', UCS ),
                ('A', AS  ),
                ('G', GBFS),
                ('H', HC)]:
  if args[0] == char:
    solver = f
assert solver != None, "invalid solver algorithm (argv[1])"

# get initial state
puzzle = [[0,0,0],[0,0,0],[0,0,0]]
for i in range(3):
  for j in range(3):
    puzzle[i][j] = eval(args[1+i*3 + j])
    assert isinstance(puzzle[i][j], int), "invalid puzzle entry (argv[2:11])"
    assert 0 <= puzzle[i][j] <= 8, "invalid puzzle entry (argv[2:11])"

# check if state is valid (no missing/repeted piece)
for k in range(9):
  found = False
  for i in range(3):
    for j in range(3):
      if puzzle[i][j] == k:
        found = True
  assert found, "invalid puzzle"

# solve puzzle
solution = solver(puzzle)
if solution:
  print(solution.depth)
  print()
  if args[-1] == 'PRINT' or args[-1] == 'print':
    solution.print_path()

else:
  print('no solution was found')