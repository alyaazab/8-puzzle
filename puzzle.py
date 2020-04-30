import copy
import queue
import heapq
import math
import sys
import datetime
import itertools

class Game:

  def __init__(self):
        self.visitSet = set()
        self.expandedNodes = []
        self.cost = -1
        self.path = []
        self.maxSearchDepth = 0
        self.executionTime = 0

  # return true if state is a goal state
  def isGoalState(self, puzzle):
    return puzzle == [[0,1,2], [3,4,5], [6,7,8]]

  # creates child node by moving one tile
  def createChild(self, zi, zj, ei, ej, puzzle):
      newPuzzle = copy.deepcopy(puzzle)
      newPuzzle[zi][zj], newPuzzle[ei][ej] = newPuzzle[ei][ej], newPuzzle[zi][zj]
      return newPuzzle

  # adds node to visited set
  def addToVisitSet(self, puzzle):
      keyPuzzle = tuple(tuple(x) for x in puzzle)
      self.visitSet.add(keyPuzzle)

  # returns true if node is already visited
  def isVisited(self, puzzle):
      keyPuzzle = tuple(tuple(x) for x in puzzle)
      return keyPuzzle in self.visitSet

  # returns true if indices are valid
  def isValid(self, i, j):
    return i>=0 and i<=2 and j>=0 and j<=2

  # returns true if puzzle state is valid
  def isValidState(self, puzzle):
    values = {'0', '1', '2', '3', '4', '5', '6', '7', '8'}
    for i in range(len(puzzle)):
      for j in range(len(puzzle[i])):
        if puzzle[i][j] in values:
          values.remove(puzzle[i][j])
        else:
          return False
    
    if len(values) > 0:
      return False
    return True
        

  # returns true if puzzle is solvable
  def isSolvable(self, puzzle):
    array = list(itertools.chain.from_iterable(puzzle))
    invCount = 0
    for i in range(8):
        for j in range(i + 1, 9):
            if array[j] != 0 and array[i] != 0 and array[i] > array[j]:
                invCount += 1
    return invCount % 2 == 0


  # returns children of a node, along with their zero indices
  def getChildren(self, puzzle, zi, zj):
    indices = []
    children = []

    # row = [0, 0, -1, 1]
    # col = [1, -1, 0, 0]
    row = [-1, 1, 0, 0]
    col = [0, 0, 1, -1]

    for i in range(4):
      if self.isValid(zi+row[i], zj+col[i]):
        children.append(self.createChild(zi, zj, zi + row[i], zj+col[i], puzzle))
        indices.append((zi+row[i], zj+col[i]))

    return children, indices

  # returns true if a node has unvisited children
  def hasUnvisitedChildren(self, puzzle, zidx):
    children, indices = self.getChildren(puzzle, zidx[0], zidx[1])
    for i in range(len(children)):
      if self.isVisited(children[i]) == False:
        return True
    return False

  # finds row and column indices of the empty tile
  def findZeroIdx(self, puzzle):
    for i in range(len(puzzle)):
      for j in range(len(puzzle)):
        if puzzle[i][j] == 0:
          return i,j
  
  def printSearchInfo(self, searchMethod):
    print("\n\n\nPath to goal")
    if searchMethod == self.dfs:
      for i in range(len(self.path)):
        self.printPuzzle(self.path[i][0])
    elif searchMethod == self.bfs:
      for i in range(len(self.path)-1, -1, -1):
        self.printPuzzle(self.path[i])
    else:
      for i in range(len(self.path)-1, -1, -1):
        self.printPuzzle(self.path[i])

    print("\nCost of Path:", len(self.path)-1)
    print("Number of Expanded Nodes:", len(self.expandedNodes))
    print("Search Depth:", len(self.path)-1)
    print("Execution Time:", self.executionTime)


  # returns Manhattan distance of a puzzle
  def getManhattanDistance(self, puzzle):
    total = 0

    for i in range(len(puzzle)):
      for j in range(len(puzzle)):
        val = puzzle[i][j]
        if val is 0:
          continue

        distance = abs(i - int(val/3)) + abs(j - val%3)
        total += distance

    return total

  # returns Euclidean distance of a puzzle
  def getEuclideanDistance(self, puzzle):
    total = 0

    for i in range(len(puzzle)):
      for j in range(len(puzzle)):
        val = puzzle[i][j]
        if val is 0:
          continue

        distance = math.sqrt((i - int(val/3))**2 + (j - val%3)**2)
        total += distance

    return total


  # performs depth-first search on a puzzle
  def dfs(self, puzzle):
    startTime = datetime.datetime.now()
    zi, zj = self.findZeroIdx(puzzle)
    stack = [(puzzle, [zi, zj])]
    
    while len(stack) > 0:
      current, zidx = stack.pop()

      if self.isVisited(current):
        continue

      self.path.append((current, zidx))
      self.expandedNodes.append(current)
      self.addToVisitSet(current)

      if self.isGoalState(current):
        endTime = datetime.datetime.now()
        self.executionTime = (endTime - startTime).total_seconds()
        return


      while(len(self.path) > 0):
        top, z = self.path[len(self.path)-1]
        if self.hasUnvisitedChildren(top, z):
          break
        self.path.pop()
     
      children, indices = self.getChildren(current, zidx[0], zidx[1])
      for i in range(len(children)):
        stack.append((children[i], indices[i]))
      
      if len(children) == 0:
        if self.cost > self.maxSearchDepth:
          self.maxSearchDepth = self.cost 
        self.cost = 0


  # performs breadth-first search on a puzzle
  def bfs(self, puzzle):
    startTime = datetime.datetime.now()
    treeMap = {}
    q = queue.Queue()
    zi, zj = self.findZeroIdx(puzzle)

    q.put((puzzle, [zi, zj]))

    while q.empty() is not True:
      currentState, zidx = q.get()

      if self.isVisited(currentState):
        continue

      self.expandedNodes.append(currentState)
      self.addToVisitSet(currentState)

      children, indices = self.getChildren(currentState, zidx[0], zidx[1])
      for i in range(len(children)):
        q.put((children[i], indices[i]))
        if self.isVisited(children[i]) == False:
          keyPuzzle = tuple(tuple(x) for x in children[i])
          treeMap[keyPuzzle] = currentState

          if self.isGoalState(children[i]):
            endTime = datetime.datetime.now()
            self.executionTime = (endTime - startTime).total_seconds()

            keyPuzzle = tuple(tuple(x) for x in children[i])
            parent = treeMap.get(keyPuzzle)
            self.path.append(children[i])

            while parent is not None:
              self.path.append(parent)
              keyPuzzle = tuple(tuple(x) for x in parent)
              parent = treeMap.get(keyPuzzle)
            return

      
  # performs A* search on a puzzle (heuristic function is passed as an argument)
  def astar(self, puzzle, heuristicFunc):
    startTime = datetime.datetime.now()
    treeMap = {}
    zeroIdx = self.findZeroIdx(puzzle)
    currentState = State(puzzle, zeroIdx, 0, 0)
    currentState.key = heuristicFunc(currentState.puzzle)

    heap = []
    heapq.heapify(heap)
    heapq.heappush(heap, currentState)
    
    while len(heap) > 0:
      currentState = heapq.heappop(heap)
      zidx = currentState.zeroIdx

      if self.isVisited(currentState.puzzle):
        continue

      
      self.expandedNodes.append(currentState)
      self.addToVisitSet(currentState.puzzle)

      if self.isGoalState(currentState.puzzle):
        endTime = datetime.datetime.now()
        self.executionTime = (endTime - startTime).total_seconds()
        
        keyPuzzle = tuple(tuple(x) for x in currentState.puzzle)
        parent = treeMap.get(keyPuzzle)
        self.path.append(currentState.puzzle)

        while parent is not None:
          self.path.append(parent)
          keyPuzzle = tuple(tuple(x) for x in parent)
          parent = treeMap.get(keyPuzzle)
        return

      children, indices = self.getChildren(currentState.puzzle, zidx[0], zidx[1])
      
      for i in range(len(children)):
        child = State(children[i], indices[i], currentState.distance+1, 0)
        child.key = heuristicFunc(child.puzzle) + child.distance
        heapq.heappush(heap, child)
        if self.isVisited(children[i]) == False:
          keyPuzzle = tuple(tuple(x) for x in children[i])
          treeMap[keyPuzzle] = currentState.puzzle
      


  def printPuzzle(self, puzzle):
    for i in range(len(puzzle)):
      print(puzzle[i])
    print()
    


class State:
  def __init__(self, puzzle, zeroIdx, distance, key):
        self.puzzle = puzzle
        self.zeroIdx = zeroIdx
        self.distance = distance
        self.key = key

  def __lt__(self, other):
        return self.key < other.key

  def __eq__(self, other):
        return self.puzzle == other.puzzle




def getInitialState(game):

  while True:
    print("Enter the initial state of your puzzle in the following format: ")
    print("0 1 2")  
    print("3 4 5")  
    print("6 7 8")
    print()
    print()

    r0 = input()
    r1 = input()
    r2 = input()

    
    puzzle = [r0.split(" "), r1.split(" "), r2.split(" ")]

    # print(game.isValidState(puzzle))
    if game.isValidState(puzzle):
      print("\n\nYour intial state:")
      puzzle = [[int(x) for x in r0.split(" ")], [int(x) for x in r1.split(" ")], [int(x) for x in r2.split(" ")] ]
      game.printPuzzle(puzzle)

      if game.isSolvable(puzzle) == False:
        print("This state is not solvable")
        sys.exit(0)

      return puzzle

    print("\nInvalid state.")


def callSearchMethod(game, puzzle):
  while True:

    print("Select a search algorithm")
    print("(1) Depth-First Search")
    print("(2) Breadth-First Search")
    print("(3) A* Search\n")

    selectedSearch = input()

    if selectedSearch == '1':
      game.dfs(puzzle)
      game.printSearchInfo(game.dfs)
      return
    elif selectedSearch == '2':
      game.bfs(puzzle)
      game.printSearchInfo(game.bfs)
      return
    elif selectedSearch == '3':
      print("Select a heuristic function")
      print("(1) Manhattan distance")
      print("(2) Euclidean distance\n")

      hfunc = input()
      if hfunc == '1':
        game.astar(puzzle, game.getManhattanDistance)
        game.printSearchInfo(game.astar)
        return
      elif hfunc == '2':
        game.astar(puzzle, game.getEuclideanDistance)
        game.printSearchInfo(game.astar)
        return


    print("Invalid Input")


def menu():
  game = Game()
  puzzle = getInitialState(game)
  callSearchMethod(game, puzzle)



menu()


