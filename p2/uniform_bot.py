from random import choice

def think(state, quip):
  return choice(state.get_moves())
