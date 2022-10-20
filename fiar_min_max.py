import time
from multiprocessing import Pool

from min_max_tree import MinMaxTree
from random import choice


class FIARMinMax:
	def __init__(self, game, *, max_depth=3, plays: int = 1, verbose=False, mt=False):
		self.game = game
		self.plays = plays  # by default, the algo plays second
		self.tree = None
		self.max_depth = max_depth
		self.mt = mt  # multithreaded processing

		# TODO: make a debug node with more debug options (useful for unit tests)
		# the list of all options with the same score on the last move
		# used for debugging when figuring out why the algo played a certain way
		self.last_play_options: list[int] = []
		self.verbose = verbose

	def debug_print(self, *args, **kwargs):
		if self.verbose:
			print(*args, **kwargs)

	def _update_tree(self):
		"""Makes sure the tree is at the right depth and all the children exist at each layer."""
		start_time = time.perf_counter()

		# TODO: implement a multithread tree generation
		# if self.mt and False:
		# 	# self.tree.generate_tree_mt(self.max_depth)
		# 	raise NotImplementedError("no multithreading yet :(")
		# else:
		self.tree.generate_tree(self.max_depth)

		self.debug_print(
			f"Updating {'(mt) ' if self.mt else ''}tree with depth {self.max_depth} "
			f"took {time.perf_counter() - start_time:.3f}s")
		pass

	@staticmethod
	def worker(child):
		return child.get_score(), child

	def get_children_scores(self, mt) -> list[tuple[float, MinMaxTree]]:
		"""Return the list of scores of the immediate children."""
		if mt:
			with Pool() as pool:
				scores = pool.map(self.worker, [child for child in self.tree.children])
		else:
			scores = [(child.get_score(), child) for child in self.tree.children]
		return scores

	def get_best_play(self):
		if not self.tree:
			self.debug_print("Generating tree...")
			self.tree = MinMaxTree(self.game.board.__copy__(), playing=self.plays)
			self._update_tree()

		self.debug_print("Calculating best move...")
		# if the current board state is not the head of the tree, find the child that corresponds
		if self.game.board != self.tree.node.board:
			for child in self.tree.children:
				if self.game.last_play == child.node.delta:
					self.tree = child
					self._update_tree()
					break

		# kinda hacky and against best practice, but it's readable and gets the work done
		better, worse = (max, min) if self.tree.node.maximizing else (min, max)

		# get a list of the best options (the children in the list are tied)
		best_children = []
		best_score = worse((-5, 5))

		# get the scores and pick the best ones
		scores = self.get_children_scores(self.mt)
		for score, child in scores:
			if score == best_score:
				best_children.append(child)

			elif better(score, best_score) == score:
				best_children = [child]
				best_score = score

		# pick a random option out of the available ones
		chosen = choice(best_children)
		self.debug_print(
			f"Chose random out of {len(best_children)} options (Score: {best_score:.2f}):"
			f" {[c.node.delta for c in best_children]}")
		self.last_play_options = [child.node.delta for child in best_children]

		# adjust the tree after the move
		self.tree = chosen

		self.debug_print("Updating the tree...")
		self._update_tree()
		self.debug_print("Your turn!")

		return chosen.node.delta
