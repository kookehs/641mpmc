def think(state, quip):
  player = state.get_whos_turn()
  max_score = state.get_score()[player]
  best_move = None;

  for move in state.get_moves():
    copy_state = state.copy()
    copy_state.apply_move(move)

    if max_score <= copy_state.get_score()[player]:
        max_score = copy_state.get_score()[player]
        best_move = move

  return best_move
