from math import log
from math import sqrt
from random import choice
from time import time

class Node:
  def __init__(self, move = None, parent = None, state = None, otherPlayer = None):
    self.move = move
    self.parentNode = parent
    self.childNodes = []
    self.score = 0
    self.visits = 0
    self.untriedMoves = state.get_moves()
    self.playerJustMoved = otherPlayer

  def UCTSelectChild(self):
    return sorted(self.childNodes, key = lambda c: float(c.score) / float(c.visits) + sqrt(2 * log(float(self.visits)) / float(c.visits)))[-1]
    # return sorted(self.childNodes, key = lambda c: c.score + sqrt(2 * log(float(self.visits)) / float(c.visits)))[-1]

  def AddChild(self, m, s, otherPlayer):
    n = Node(move = m, parent = self, state = s, otherPlayer = otherPlayer)
    self.untriedMoves.remove(m)
    self.childNodes.append(n)

    return n

  def Update(self, result):
    self.visits += 1
    self.score += result

def UCT(rootstate, quip):
  start = time()
  elapsed = 0
  opposite = {"blue" : "red", "red" : "blue"}
  currentPlayer = rootstate.get_whos_turn()
  rootnode = Node(state = rootstate, otherPlayer = opposite[currentPlayer])
  iterations = 0

  while elapsed < 1:
    node = rootnode
    state = rootstate.copy()

    while node.untriedMoves == [] and node.childNodes != []:
      node = node.UCTSelectChild()
      state.apply_move(node.move)

    if node.untriedMoves != []:
      move = choice(node.untriedMoves)
      current = state.get_whos_turn()
      state.apply_move(move)
      node = node.AddChild(m = move, s = state, otherPlayer = current)

    depth = 0

    while state.get_moves() != []:
      state.apply_move(choice(state.get_moves()))
      depth += 1

    scores = state.get_score()

    while node != None:
      # node.Update(result = scores[node.playerJustMoved])
      node.Update(result = scores[node.playerJustMoved] - scores[opposite[node.playerJustMoved]])
      node = node.parentNode

    elapsed = time() - start
    iterations += 1

  quip("DEPTH: " + str(depth))
  quip("ELAPSED: " + str(elapsed))
  quip("ITERATIONS/SECOND: " + str(iterations / elapsed))

  return sorted(rootnode.childNodes, key = lambda c: c.visits)[-1].move

def think(state, quip):
    return UCT(state, quip)
