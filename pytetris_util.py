# <add info header here>

import sys, pygame 
from game import Game

#globals
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
FPS = 50

BLACK = 0, 0, 0
WHITE = 255, 255, 255

# Arduino config
SERIAL_PORT = '/dev/ttyACM0'
BAUD_RATE = 9600

# helpers
def print_welcome(msg):
	print(msg)
	return

def get_player_ready(prompt):
	ok = False
	while not ok:
		user_response = input(prompt)  # ask user if they're ready to play
		begin, ok = validate_user_response(user_response)
	return begin


def validate_user_response(user_response):
	player_ready = False
	valid_response = False
	if len(user_response) > 0:
		user_response = user_response[0]

		if user_response.isalpha():
			user_response = user_response.lower()
			
			if user_response in ("y", "n"):
				valid_response = True
				player_ready = user_response == "y"

	return player_ready, valid_response


def update_score_display(game):
	pygame.display.set_caption("pytetris | player score: %s" % (game.player_score))


def exit_with_msg(msg):
	print(msg)
	sys.exit()


def startup_tetris():
	# global TEST_ser_thread

	pygame.init()
	pygame.key.set_repeat(100, FPS//2)  # enable key repeats every half a frame
	
	# ser = None 
	# try: 
	# 	ser = serial.Serial(SERIAL_PORT, BAUD_RATE)
	# except:
	# 	print("[DEBUG] startup: Couldn't connect to serial port", SERIAL_PORT)
	# 	pass

	game = Game(pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)), pygame.time.Clock())
	
	update_score_display(game)
	
	# TEST_ser_thread = WorkerThread(ser_worker, game.serial_port)
	# TEST_ser_thread.start()

	return game


# main game processing


# update game state here
def update(game):
	pass


def check_events(game):
	global TEST_ser_thread
	with LOCK:# TEST
		pygame.event.pump() # TEST
		for event in pygame.event.get():
			pass
			# if event.type == pygame.QUIT:
			# 	print("trying to stop worker thread:", TEST_ser_thread)
			# 	TEST_ser_thread.stop_worker_thread()
			# 	# TEST_ser_thread.stop = True
			# 	# TEST_ser_thread.join()
			# 	sys.exit()

			# elif event.type == pygame.KEYDOWN:
			# 	# if DEBUG:
			# 	# 	print("KEYDOWN event for key %s" % (event.key))
				
			# 	if event.key == pygame.K_ESCAPE:
			# 		TEST_ser_thread.stop_worker_thread()
			# 		sys.exit()

			# 	if event.key in (pygame.K_w,pygame.K_UP):
			# 		if game.objects[0].y - 5 >= 0:
			# 			game.objects[0].y -= 5
			# 		else:
			# 			game.objects[0].y = 0

			# 	if event.key in (pygame.K_a, pygame.K_LEFT):
			# 		if game.objects[0].x - 5 >= 0:
			# 			game.objects[0].x -= 5
			# 		else:
			# 			game.objects[0].x = 0

			# 	if event.key in (pygame.K_s, pygame.K_DOWN):
			# 		if game.objects[0].y + game.objects[0].length + 5 <= SCREEN_HEIGHT:
			# 			game.objects[0].y += 5
			# 		else:
			# 			game.objects[0].y = SCREEN_HEIGHT - game.objects[0].length

			# 	if event.key in (pygame.K_d, pygame.K_RIGHT):
			# 		if game.objects[0].x + game.objects[0].width + 5 <= SCREEN_WIDTH:
			# 			game.objects[0].x += 5
			# 		else:
			# 			game.objects[0].x = SCREEN_WIDTH - game.objects[0].width

			# elif event.type == pygame.USEREVENT: # TEST
			# 	print(event.code)


def render(game):
	game.clear_window()
	game.draw_objects()

	# update frame
	pygame.display.flip()
