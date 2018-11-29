# <put class header info here>
import graphics, random

class Game:
	backgroundColor = (0, 0, 0)
	def __init__(self, window, tile_size, tiles_width, tiles_height, clock):
		self.window = window 	# draw game interface 
		# self.grid = []
		self.tile_size = tile_size
		self.init_grid(tiles_width, tiles_height)		# get grid filled with None
		self.active_shape = None
		self.clock = clock   	# control game speed
		self.player_score = 0
		self.paused = False
		self.game_over = False
		self.rgen = random.Random() # get a new seed every time

	# create a new random shape with a random color
	def spawn_new_shape(self):
		shapes = graphics.shapes.get_shapes()
		rand_shape_type = shapes[self.rgen.randint(0,len(shapes)-1)]
		rand_color = self.get_rand_color()

		# make sure each shape started in the top centre of the window
		if rand_shape_type == graphics.shapes.square: 
			location = (4*self.tile_size,0)
			new_shape = graphics.square(location, rand_color, self.tile_size, self.window)
		
		elif rand_shape_type ==  graphics.shapes.rectangle:
			location = (3*self.tile_size,0)
			new_shape = graphics.rectangle(location, rand_color, self.tile_size, self.window)
		
		elif rand_shape_type == graphics.shapes.tee:
			location = (4*self.tile_size,0)
			new_shape = graphics.tee(location, rand_color, self.tile_size, self.window)
		
		elif rand_shape_type == graphics.shapes.leftz:
			location = (4*self.tile_size,0)
			new_shape = graphics.leftz(location, rand_color, self.tile_size, self.window)
		
		elif rand_shape_type == graphics.shapes.rightz:
			location = (4*self.tile_size,0)
			new_shape = graphics.rightz(location, rand_color, self.tile_size, self.window)
		
		elif rand_shape_type == graphics.shapes.leftl:
			location = (4*self.tile_size,0)
			new_shape = graphics.leftl(location, rand_color, self.tile_size, self.window)
		
		elif rand_shape_type == graphics.shapes.rightl:
			location = (4*self.tile_size,0)
			new_shape = graphics.rightl(location, rand_color, self.tile_size, self.window)
		
		else:
			raise TypeError("Unrecognized shape %s specified." % (rand_shape_type))

		self.active_shape = new_shape


	def unpack_active_shape(self):
		pass


	def get_rand_color(self):
		return (self.rgen.randint(0, 255), self.rgen.randint(0, 255), self.rgen.randint(0, 255))


	def init_grid(self, tiles_width, tiles_height):
		self.grid = []
		for x in range(tiles_width):
			self.grid.append([])
			for y in range(tiles_height):
				self.grid[x].append(None)


	def get_object_locations(self):
		shape_blocks_locs = [b.location for b in self.active_shape.blocks]
		grid_blocks_locs = [b.location for b in self.get_grid_blocks]
		locs = [shape_blocks_locs]
		for i in range(len(grid_blocks_locs)):
			locs.append(grid_blocks_locs[i])
		
		return locs

	
	def get_grid_blocks(self):
		# Assumption: all objects in self.grid are either None or type graphics.block
		return [b for b in self.grid if b]