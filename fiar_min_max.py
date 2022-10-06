from min_max_tree import MinMaxTree


class FIARMinMax:
	def __init__(self, game, *, max_depth=3, plays: int = 1):
		self.game = game
		self.plays = plays  # by default, the algo plays second
		self.tree = None
		self.max_depth = max_depth

	def get_best_play(self):
		if not self.tree:
			self.tree = MinMaxTree(self.game.board, playing=self.plays)
			self.tree.generate_tree(self.max_depth)

		# kinda hacky and against best practice, but it's readable and gets the work done
		func = max if self.tree.node.maximizing else min
		best_child: MinMaxTree = func(self.tree.children, key=lambda c: c.get_score())

		return best_child.node.delta
