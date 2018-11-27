# <put class header info here>
class Game:
	backgroundColor = (0, 0, 0)
	def __init__(self, window, clock):
		self.window = window 	# draw game interface 
		self.objects = []    	# store all objects for the game
		self.clock = clock   	# control game speed
		self.player_score = 0
		self.paused = False
		self.game_over = False

	def clear_window(self):
		# clear window
		self.window.fill(backgroundColor)

	def draw_objects(self):
		# draw stuff
		for o in self.objects:
			try:
				o.draw()
			except AttributeError:
				print("object did not have a draw method.")
 