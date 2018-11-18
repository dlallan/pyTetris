import pygame, serial, sys

# Globals
DEBUG = True

BLACK = 0, 0, 0
WHITE = 255, 255, 255

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
FPS = 50

# Arduino config
SERIAL_PORT = '/dev/ttyACM0'
BAUD_RATE = 9600
PIN_RIGHT = 6
PIN_DOWN = 7
PIN_UP = 8
PIN_LEFT = 9
PINS = [PIN_RIGHT, PIN_DOWN, PIN_UP, PIN_LEFT]


class Game:
	def __init__(self, window, clock, serial_port):
		self.window = window
		self.objects = [] # store all objects for the game here
		self.clock = clock
		self.serial_port = serial_port

	def clear_window(self):
		# clear window
		self.window.fill((0, 0, 0))

	def draw_objects(self):
		# draw stuff
		for o in self.objects:
			try:
				o.draw()
			except AttributeError:
				print("object did not have a draw method.")


class Box:
	def __init__(self, window, color, x, y, width, length):
		self.window = window
		self.color = color
		self.x = x
		self.y = y
		self.length = length
		self.width = width


	def draw(self):
		# if DEBUG:
		# 	print(self.x, self.y)
			# print(self.rect[0], self.rect[1])
		pygame.draw.rect(self.window, self.color, self.get_rect())

	
	def get_rect(self):
		return [self.x, self.y, self.width, self.length]


def check_events(game):
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			if DEBUG:
				print("KEYDOWN event for key %s" % (event.key))
			
			if event.key == pygame.K_ESCAPE:
				sys.exit()

			if event.key in (pygame.K_w,pygame.K_UP):
				if game.objects[0].y - 5 >= 0:
					game.objects[0].y -= 5
				else:
					game.objects[0].y = 0

			if event.key in (pygame.K_a, pygame.K_LEFT):
				if game.objects[0].x - 5 >= 0:
					game.objects[0].x -= 5
				else:
					game.objects[0].x = 0

			if event.key in (pygame.K_s, pygame.K_DOWN):
				if game.objects[0].y + game.objects[0].length + 5 <= SCREEN_HEIGHT:
					game.objects[0].y += 5
				else:
					game.objects[0].y = SCREEN_HEIGHT - game.objects[0].length

			if event.key in (pygame.K_d, pygame.K_RIGHT):
				if game.objects[0].x + game.objects[0].width + 5 <= SCREEN_WIDTH:
					game.objects[0].x += 5
				else:
					game.objects[0].x = SCREEN_WIDTH - game.objects[0].width

		elif event.type == pygame.USEREVENT:
			print(event.code)


def update(game):
	# ev = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_w})
	# ev = pygame.event.Event(pygame.USEREVENT, {'code': 'this is a test.'})
	# pygame.event.post(ev)

	# poll serial
	try:
		pin, state = poll_serial(game)
	# if button is DOWN, trigger KEYDOWN event
	# if button is UP, trigger KEYUP event
	except: # couldn't get pin state
		pass
		


def poll_serial(game):
	line = "".join(map(chr, game.serial_port.readline()))
	line = line.split(',')
	if len(line) == 1: # skip fragmented lines
		return None
	
	if DEBUG:
		print(line[0], line[1].rstrip('\n\r'))

	return line

def render(game):
	game.clear_window()
	game.draw_objects()

	# update frame
	pygame.display.flip()


def center_box(box):
	box.x = SCREEN_WIDTH//2 - box.width//2
	box.y = SCREEN_HEIGHT//2 - box.length//2


def loop(game):
	# clock = pygame.time.Clock()
	# box = Box(window, WHITE, 0, 0, 50, 50)
	center_box(game.objects[0])
	# objects = [box,]

	if DEBUG:
		print("key repeat (ms): ", pygame.key.get_repeat())

	while True:
		game.clock.tick(FPS)
		check_events(game)
		update(game)
		render(game)


def startup():
	pygame.init()
	game = Game(pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)),
				pygame.time.Clock(),
				serial.Serial(SERIAL_PORT, BAUD_RATE))

	game.objects.append(Box(game.window, WHITE, 0, 0, 50, 50))
	
	# window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
	pygame.display.set_caption("Event Test")
	pygame.key.set_repeat(100, FPS//2)
	
	# ser = serial.Serial('/dev/ttyACM0', 9600) # listen to input from an Arduino

	return game


def main():
	game = startup()
	loop(game)


if __name__ == '__main__':
	main()
