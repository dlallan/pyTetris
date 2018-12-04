"""
----------------------------------------------------------
Name: Dillon Allan, Ian Yurychuk
ID: 1350542, 1552809
CMPUT 274, Fall 2018

Final Project: pytetris - Python implementation of Tetris
----------------------------------------------------------
The file game.py contains a single class Game, which is used to capture the state of 
pytetris during runtime. It contains attributes for tile size, screen width/height in 
tiles, clock, active shape, and grid, which tracks shapes when they stop falling. It 
contains methods that are used for spawning new active shapes, "unpacking" the active 
shape into the grid, collision deteection, and dropping filled rows.

Refer to the README for more information.
"""
import graphics, pygame, random

# globals
DEBUG = False  # set to False before submission!


class Game:
	'''Main class for tracking a game of tetris.'''
	backgroundColor = (0, 0, 0)
	def __init__(self, window, tile_size, tiles_width, tiles_height, clock):
		self.window = window 								 # draw game interface 
		self.tile_size = tile_size 							 # all movements in the game are multiples of tile_size
		self.tiles_width = tiles_width 						 # screen width in tiles
		self.tiles_height = tiles_height 					 # screen height in tiles
		self.init_grid(self.tiles_width, self.tiles_height)  # get grid filled with None
		self.active_shape = None 							 # let user choose when the active shape is first spawned
		self.clock = clock   	 							 # control game speed
		self.player_score = 0
		self.paused = False
		self.game_over = False
		self.rgen = random.Random() 						 # used for random shapes and colors
		self.move_down_event = pygame.USEREVENT + 1 		 # get ID for event handling falling shape

	def spawn_new_shape(self):
		'''create a new random shape with a random color'''
		shapes = graphics.shapes.get_shapes()
		rand_shape_type = shapes[self.rgen.randint(0,len(shapes)-1)]
		rand_color = self.get_rand_color()

		# make sure each shape starts in the top centre of the window
		if rand_shape_type == graphics.shapes.square: 
			location = [4*self.tile_size,0]
			new_shape = graphics.square(location, rand_color, self.tile_size, self.window)
		
		elif rand_shape_type ==  graphics.shapes.rectangle:
			location = [3*self.tile_size,0]
			new_shape = graphics.rectangle(location, rand_color, self.tile_size, self.window)
		
		elif rand_shape_type == graphics.shapes.tee:
			location = [4*self.tile_size,0]
			new_shape = graphics.tee(location, rand_color, self.tile_size, self.window)
		
		elif rand_shape_type == graphics.shapes.leftz:
			location = [4*self.tile_size,0]
			new_shape = graphics.leftz(location, rand_color, self.tile_size, self.window)
		
		elif rand_shape_type == graphics.shapes.rightz:
			location = [4*self.tile_size,0]
			new_shape = graphics.rightz(location, rand_color, self.tile_size, self.window)
		
		elif rand_shape_type == graphics.shapes.leftl:
			location = [4*self.tile_size,0]
			new_shape = graphics.leftl(location, rand_color, self.tile_size, self.window)
		
		elif rand_shape_type == graphics.shapes.rightl:
			location = [4*self.tile_size,0]
			new_shape = graphics.rightl(location, rand_color, self.tile_size, self.window)
		
		else:
			raise TypeError("Error: unrecognized shape specified: %s" % (rand_shape_type))

		self.active_shape = new_shape


	def unpack_active_shape(self):
		'''move all blocks from active shape to the grid, where each 
		block's location coords map to the row/col coords of the grid.'''
		for b in self.active_shape.blocks: 
			row = b.location[1] // b.block_dim
			col = b.location[0] // b.block_dim
			self.grid[row][col] = b  


	def get_rand_color(self):
		'''Return random colors in an RGB range that makes them not too bright or dark.'''
		return (self.rgen.randint(25, 225), self.rgen.randint(25, 225), self.rgen.randint(25, 225))


	def init_grid(self, tiles_width, tiles_height):
		'''Null-initialize the grid to be a list of length tiles_height
		containing lists of of length tiles_width.''' 
		self.grid = []
		for row in range(tiles_height):
			self.grid.append([])
			for col in range(tiles_width):
				self.grid[row].append(None)


	def get_active_shape_block_locs(self):
		'''Get a list of locations for every block in the active (falling) shape.'''
		if self.active_shape:
			return [b.location for b in self.active_shape.blocks]


	def copy_active_shape_block_locs(self):
		'''Copy and return the locations of every block in the active (falling) shape. '''
		if self.active_shape:
			return [list(b.location) for b in list(self.active_shape.blocks)]


	def get_object_locations_as_Rects(self):
		'''Get a list locations as pygame Rects for the grid blocks and active shape,'''
		locs = []
		shape_blocks_locs = self.get_active_shape_block_locs()
		for i in range(len(shape_blocks_locs)):
			locs.append(pygame.Rect(shape_blocks_locs[i], (self.tile_size, self.tile_size)))

		grid_blocks_locs = self.get_grid_blocks_locs()
		for i in range(len(grid_blocks_locs)):
			locs.append(pygame.Rect(grid_blocks_locs[i], (self.tile_size, self.tile_size)))
		
		return locs


	def get_grid_block_locs_as_Rects(self):
		'''Get a list of pygame Rects describing the grid blocks.'''
		rects = []
		for row in range(len(self.grid)):
			for col in range(len(self.grid[row])):
				b = self.grid[row][col] 
				if b: # check if block exists at this grid position
					rects.append(pygame.Rect(b.location, (b.block_dim, b.block_dim)))		

		return rects


	def check_for_collisions(self):
		'''Go over each block in the active shape
		and test if it overlaps with any blocks in the grid.'''
		grid_rects = self.get_grid_block_locs_as_Rects()

		for b in self.active_shape.blocks:
			b_rect = pygame.Rect(b.location, (b.block_dim, b.block_dim))
			if b_rect.collidelist(grid_rects) != -1:
				return True

		return False


	def get_grid_blocks_locs(self):
		'''Get a list of locations for every block in the grid.
		Can be empty if no blocks exist in the grid.'''

		# Assumption: all objects in self.grid are either None or type graphics.block
		locs = []
		for row in range(len(self.grid)):
			for col in range(len(self.grid[row])):
				b = self.grid[row][col] 
				if b: # check if block exists at this grid position
					locs.append(b.location)
		
		return locs


	def get_rows_filled(self):
		'''Go over each row in the grid and retrieve the row indices
		for rows filled with blocks.'''
		filled_rows = []

		for row in range(len(self.grid)):
			if DEBUG:
				print("TEST",row, self.grid[row])
			
			if all([col for col in self.grid[row]]): # ASSUMPTION: col is either block or None
				if DEBUG:
					print ("row", row, "is full")
				
				filled_rows.append(row)

		return filled_rows


	def try_drop_filled_rows(self):
		'''Attempt to remove filled rows from the grid.
		Does nothing if no rows are filled.'''
		filled_rows = self.get_rows_filled() # get filled rows (could get nothing)
		if DEBUG:
			print("Filled rows:", filled_rows)

		for row in range(len(self.grid)):
			if row in filled_rows:
				del self.grid[row]
				self.grid.insert(0, self.get_new_row())  # insert blank row at top of grid
				self.shift_rows_down(row)  # move rows above filled row down one block

		return len(filled_rows) # indicate how many rows were deleted


	def shift_rows_down(self, row):
		'''Increment y coordinates of all blocks in the range [0,row].'''
		
		# go over all rows above and including grid[row]
		for row in range(row,-1,-1):
			if DEBUG:
				print("at row", row)
			for block in self.grid[row]:
				if block:  # shift blocks down
					block.location[1] += block.block_dim


	def get_new_row(self):
		'''Return a null-initialized list of length tiles_width.'''
		return [None] * self.tiles_width
