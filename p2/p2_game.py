
class Game(object):
	def __init__(self, width):
		self.width = width
		self.players = ('red','blue') # these must be valid tkinter color names
		self.dots = frozenset((i,j) for i in range(self.width) for j in range(self.width))
		self.boxes = frozenset((i,j) for i in range(self.width-1) for j in range(self.width-1))
		self.h_lines = frozenset((i,j) for i in range(self.width-1) for j in range(self.width))
		self.v_lines = frozenset((i,j) for i in range(self.width) for j in range(self.width-1))

class State(object):
	def __init__(self, game):
		self.game = game
		self.whos_turn = game.players[0]
		self.box_owners = {}
		self.h_line_owners = {}
		self.v_line_owners = {}

	def copy(self):
		res = State(self.game)
		res.whos_turn = self.whos_turn
		res.box_owners = self.box_owners.copy()
		res.h_line_owners = self.h_line_owners.copy()
		res.v_line_owners = self.v_line_owners.copy()
		return res

	def get_whos_turn(self):
		return self.whos_turn

	def get_moves(self):
		h_moves = [('h', h) for h in self.game.h_lines if h not in self.h_line_owners]
		v_moves = [('v', v) for v in self.game.v_lines if v not in self.v_line_owners]
		return h_moves + v_moves

	def apply_move(self, move):

		orientation, cell = move

		if orientation == 'h':
			self.h_line_owners[cell] = self.whos_turn
		elif orientation == 'v':
			self.v_line_owners[cell] = self.whos_turn

		new_boxes = 0
		for box in self.game.boxes:
			(i,j) = box

			if 	(i,j) not in self.box_owners \
				and	(i,j) in self.h_line_owners \
				and (i,j) in self.v_line_owners \
				and (i,j+1) in self.h_line_owners \
				and (i+1,j) in self.v_line_owners:
					new_boxes += 1
					self.box_owners[box] = self.whos_turn

		if new_boxes == 0:
			self.whos_turn = self.game.players[(self.game.players.index(self.whos_turn)+1) % len(self.game.players)]

	def is_terminal(self):
		return len(self.box_owners) == len(self.game.boxes)

	def get_score(self):
		return {p: sum([1 for box in self.game.boxes if self.box_owners.get(box) is p]) for p in self.game.players}

