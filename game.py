# <put class header info here>
import graphics, pygame, random

class Game:
	backgroundColor = (0, 0, 0)
	def __init__(self, window, tile_size, tiles_width, tiles_height, clock):
		self.window = window 	# draw game interface 
		# self.grid = []
		self.tile_size = tile_size
		self.tiles_width = tiles_width
		self.tiles_height = tiles_height
		self.init_grid(self.tiles_width, self.tiles_height)		# get grid filled with None
		self.active_shape = None
		self.clock = clock   	# control game speed
		self.player_score = 0
		self.paused = False
		self.game_over = False
		self.rgen = random.Random() # get a new seed every time
		self.move_down_event = pygame.USEREVENT + 1 # get ID for the custom pygame event

	# create a new random shape with a random color
	def spawn_new_shape(self):
		shapes = graphics.shapes.get_shapes()
		rand_shape_type = shapes[self.rgen.randint(0,len(shapes)-1)]
		rand_color = self.get_rand_color()

		# make sure each shape started in the top centre of the window
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
		# move all blocks from active shape to the grid
		for b in self.active_shape.blocks: 
			row = b.location[1] // b.block_dim
			col = b.location[0] // b.block_dim
			# print((int(yloc/block_dim)-1), (int(xloc/block_dim)-1))
			self.grid[row][col] = b  

			# graphics.block(location, current_block.color, block_dim, gameDisplay)
			# all_blocks.append(graphics.block(location, current_block.color, block_dim, gameDisplay))


	def get_rand_color(self):
		return (self.rgen.randint(100, 200), self.rgen.randint(100, 200), self.rgen.randint(100, 200))


	def init_grid(self, tiles_width, tiles_height):
		self.grid = []
		for row in range(tiles_height):
			self.grid.append([])
			for col in range(tiles_width):
				self.grid[row].append(None)


	def get_active_shape_block_locs(self):
		if self.active_shape:
			return [b.location for b in self.active_shape.blocks]


	def copy_active_shape_block_locs(self):
		if self.active_shape:
			return [list(b.location) for b in list(self.active_shape.blocks)]


	def get_object_locations_as_Rects(self):
		locs = []
		shape_blocks_locs = self.get_active_shape_block_locs()
		for i in range(len(shape_blocks_locs)):
			# print(shape_blocks_locs[i], (self.tile_size, self.tile_size))
			locs.append(pygame.Rect(shape_blocks_locs[i], (self.tile_size, self.tile_size)))

		grid_blocks_locs = self.get_grid_blocks_locs()
		for i in range(len(grid_blocks_locs)):
			locs.append(pygame.Rect(grid_blocks_locs[i], (self.tile_size, self.tile_size)))
		
		return locs


	def get_grid_block_locs_as_Rects(self):
		rects = []
		for row in range(len(self.grid)):
			for col in range(len(self.grid[row])):
				# print(row,col)
				b = self.grid[row][col] 
				if b: # check if block exists at this grid position
					rects.append(pygame.Rect(b.location, (b.block_dim, b.block_dim)))		

		return rects


	def check_for_collisions(self):
		# go over each block in active shape
		# and test if it overlaps with any blocks in the grid.
		grid_rects = self.get_grid_block_locs_as_Rects()

		for b in self.active_shape.blocks:
			b_rect = pygame.Rect(b.location, (b.block_dim, b.block_dim))
			if b_rect.collidelist(grid_rects) != -1:
				return True

		return False


	def get_grid_blocks_locs(self):
		# Assumption: all objects in self.grid are either None or type graphics.block
		locs = []
		for row in range(len(self.grid)):
			for col in range(len(self.grid[row])):
				# print(row,col)
				b = self.grid[row][col] 
				if b: # check if block exists at this grid position
					locs.append(b.location)
		
		return locs


	def get_rows_filled(self):
		# go over each row in the grid and retrieve the row indices
		# for rows filled with blocks.
		filled_rows = []

		# print(len(self.grid))
		# print(self.get_grid_blocks_locs())
		for row in range(len(self.grid)):
			print("TEST",row, self.grid[row])
			if all([col for col in self.grid[row]]): # ASSUMPTION: col is either block or None
				print ("row", row, "is full")
				filled_rows.append(row)

		return filled_rows


	def try_drop_filled_rows(self):
		filled_rows = self.get_rows_filled() # get filled rows (could get nothing)
		print("Filled rows:", filled_rows)
		# add new empty row to beginning of grid, then delete the row
		
		# self.grid = [self.grid[row] for row in range(len(self.grid)) if row not in filled_rows]
		# insert new blank row at top of grid for each filled row
		# for row in filled_rows:
		for row in range(len(self.grid)):
			if row in filled_rows:
				del self.grid[row]
				self.grid.insert(0, self.get_new_row())
				self.shift_rows_down(row)

		# update all block locations above the lowest filled row
		# if filled_rows:
			# print("shifting rows down from", filled_rows[-1], "upward...")
			# self.shift_rows_down(filled_rows[-1])
			# print(self.get_grid_blocks_locs())

		return len(filled_rows) # indicate how many rows were deleted
	

	def shift_rows_down(self, row):
		# go over all rows above grid[end]
		for row in range(row,-1,-1):
			print("at row", row)
			for block in self.grid[row]:
				if block: # shift blocks down
					print("moving block in row", row) 
					block.location[1] += block.block_dim


	def get_new_row(self):
		return [None] * self.tiles_width
