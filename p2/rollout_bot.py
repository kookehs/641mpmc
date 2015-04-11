import random

ROLLOUTS = 10
MAX_DEPTH = 5

def think(state, quip):

	moves = state.get_moves()

	best_move = moves[0]
	best_expecation = float('-inf')

	me = state.get_whos_turn()

	def outcome(score):
		if me == 'red':
			return score['red'] - score['blue']
		else:
			return score['blue'] - score['red']

	for move in moves:

		total_score = 0.0

		for r in range(ROLLOUTS):

			rollout_state = state.copy()

			rollout_state.apply_move(move)


			for i in range(MAX_DEPTH):
				if rollout_state.is_terminal():
					break
				rollout_move = random.choice( rollout_state.get_moves() )
				rollout_state.apply_move( rollout_move )

			total_score += outcome(rollout_state.get_score())

		expectation = float(total_score)/ROLLOUTS

		if expectation > best_expecation:
			best_expecation = expectation
			best_move = move

	print "Picking %s with expected score %f" % (str(best_move), best_expecation)
	return best_move