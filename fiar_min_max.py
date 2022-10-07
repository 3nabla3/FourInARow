from min_max_tree import MinMaxTree
from random import choice


class FIARMinMax:
	def __init__(self, game, *, max_depth=3, plays: int = 1):
		self.game = game
		self.plays = plays  # by default, the algo plays second
		self.tree = None
		self.max_depth = max_depth

	def _update_tree(self):
		"""Makes sure the tree is at the right depth and all the children exist at each layer."""
		self.tree.generate_tree(self.max_depth)

	def get_best_play(self):
		if not self.tree:
			print("Generating tree...")
			self.tree = MinMaxTree(self.game.board.__copy__(), playing=self.plays)
			self._update_tree()
			print("Done!")

		# if the current board state is not the head of the tree, find the child that corresponds
		if self.game.board != self.tree.node.board:
			for child in self.tree.children:
				if self.game.last_play == child.node.delta:
					self.tree = child
					self._update_tree()
					break

		# kinda hacky and against best practice, but it's readable and gets the work done
		better = max if self.tree.node.maximizing else min
		worse = min if self.tree.node.maximizing else max

		# get a list of the best options (the children in the list are tied)
		best_children = []
		best_score = worse((-5, 5))
		for child in self.tree.children:
			score = child.get_score()
			if score == best_score:
				best_children.append(child)

			# if the child is better than any previous
			elif better((best_score, score)) == score:
				best_children = [child]
				best_score = score

		# pick a random option out of the available ones
		chosen = choice(best_children)
		print(f"Chose random out of {len(best_children)} options: {[c.node.delta for c in best_children]}")

		# adjust the tree after the move
		self.tree = chosen
		self._update_tree()

		return chosen.node.delta
