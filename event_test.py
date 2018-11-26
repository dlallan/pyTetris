import pygame, serial, sys, threading, time

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
NUM_PIN_STATE = 8

# TEST_ser_thread = threading.Thread(target=ser_worker, args=[game.serial_port])
TEST_ser_thread = None;#WorkerThread(ser_worker, [game.serial_port])
LOCK = threading.Lock() # TEST


class WorkerThread(threading.Thread):
	"""docstring for WorkerThread"""
	def __init__(self, mytarget=None, *myargs):
		super(WorkerThread, self).__init__(target=mytarget, args=myargs)
		self.stop = False
		print("WorkerThread has stop value: ", self.stop)
	
	def stop_worker_thread(self):
		self.stop = True
		

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
	global TEST_ser_thread
	with LOCK:# TEST
		pygame.event.pump() # TEST
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				print("trying to stop worker thread:", TEST_ser_thread)
				TEST_ser_thread.stop_worker_thread()
				# TEST_ser_thread.stop = True
				# TEST_ser_thread.join()
				sys.exit()

			elif event.type == pygame.KEYDOWN:
				if DEBUG:
					print("KEYDOWN event for key %s" % (event.key))
				
				if event.key == pygame.K_ESCAPE:
					TEST_ser_thread.stop_worker_thread()
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

			elif event.type == pygame.USEREVENT: # TEST
				print(event.code)
		
		# pygame.event.clear() # test


# update game state here
def update(game):
	pass
# 	# ev = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_w})
# 	# ev = pygame.event.Event(pygame.USEREVENT, {'code': 'this is a test.'})
# 	# pygame.event.post(ev)

# 	# poll serial
# 	# try:
# 	pinStates = poll_serial(game)
# 	# if DEBUG:
# 	# 	print(pinStates)
# 	if pinStates is None:
# 		if DEBUG:
# 			print("pinStates was empty")
# 		pass
# 	else:	
# 		# if DEBUG:
# 		# 	print(pinStates)

# 		for i in range(len(pinStates)):
# 			# get key from index i
# 			if i == 0:  # 0 --> pin RIGHT
# 				key = pygame.K_RIGHT
# 			elif i == 1:  # 1 --> pin DOWN
# 				key = pygame.K_DOWN
# 			elif i == 2:  # 2 --> pin UP
# 				key = pygame.K_UP
# 			elif i == 3:  # 3 --> pin LEFT
# 				key = pygame.K_LEFT
# 			else:
# 				raise Exception("Invalid index %s" % (i))
			
# 			# if button is DOWN, trigger KEYDOWN event
# 			if DEBUG:
# 				print("Pin state %s is %s" % (i,pinStates[i]))

# 			if not pinStates[i]: # 0 means button is DOWN
# 				ev = pygame.event.Event(pygame.KEYDOWN, {'key': key})
# 				pygame.event.post(ev)
# 				if DEBUG:
# 					print("Posted KEYDOWN event for key: %s" % (key))


def poll_serial(serial_port):
	line = "".join(map(chr, serial_port.readline()))
	line = line.split(',')

	if len(line) == NUM_PIN_STATE: # ignore fragmented lines
		line[-1] = line[-1].rstrip() # strip newline from last element
		line = [bool(int(val)) for val in line[1::2]] # get the states only
		# if DEBUG:
		# 	print(line)
		return line
	else:
		return None

def ser_worker(serial_port):
	t = threading.currentThread()
	print("serial_port arg:", serial_port)
	while(not t.stop):
		pinStates = poll_serial(serial_port)
		# if DEBUG:
		# 	print(pinStates)
		if pinStates is None:
			if DEBUG:
				print("pinStates was empty")
			pass
		else:	
			if DEBUG:
				print(pinStates)

			with LOCK: # TEST
				for i in range(len(pinStates)):
					# get key from index i
					if i == 0:  # 0 --> pin RIGHT
						key = pygame.K_RIGHT
					elif i == 1:  # 1 --> pin DOWN
						key = pygame.K_DOWN
					elif i == 2:  # 2 --> pin UP
						key = pygame.K_UP
					elif i == 3:  # 3 --> pin LEFT
						key = pygame.K_LEFT
					else:
						raise Exception("Invalid index %s" % (i))
					
					# if button is DOWN, trigger KEYDOWN event
					# if DEBUG:
						# print("Pin state %s is %s" % (i,pinStates[i]))

					if not pinStates[i]: # 0 means button is DOWN
						ev = pygame.event.Event(pygame.KEYDOWN, {'key': key})
						pygame.event.post(ev)
						if DEBUG:
							print("Posted KEYDOWN event for key: %s" % (key))
		t = threading.currentThread()

		time.sleep(0.1)  # keep thread from pinning
	if DEBUG:
		print("Exiting worker thread...")


def render(game):
	game.clear_window()
	game.draw_objects()

	# update frame
	pygame.display.flip()


def center_box(box):
	box.x = SCREEN_WIDTH//2 - box.width//2
	box.y = SCREEN_HEIGHT//2 - box.length//2


def loop(game):
	center_box(game.objects[0])

	if DEBUG:
		print("key repeat (ms): ", pygame.key.get_repeat())

	while True:
		game.clock.tick(FPS)
		check_events(game)
		# update(game)
		render(game)


def startup():
	global TEST_ser_thread

	pygame.init()
	ser = None 
	try: 
		ser = serial.Serial(SERIAL_PORT, BAUD_RATE)
	except:
		print("[DEBUG] startup: Couldn't connect to serial port", SERIAL_PORT)
		pass

	game = Game(pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)),
				pygame.time.Clock(),
				ser)

	game.objects.append(Box(game.window, WHITE, 0, 0, 50, 50)) # make a white box
	
	pygame.display.set_caption("Event Test")
	pygame.key.set_repeat(100, FPS//2)  # enable key repeats every half a frame

	
	TEST_ser_thread = WorkerThread(ser_worker, game.serial_port)
	TEST_ser_thread.start()

	return game


def main():
	game = startup()
	loop(game)


if __name__ == '__main__':
	main()
