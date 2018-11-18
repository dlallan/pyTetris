import pygame, sys

# Globals
DEBUG = True

BLACK = 0, 0, 0
WHITE = 255, 255, 255

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
FPS = 50

class Box:
	def __init__(self, window, color, x, y, width, length):
		self.window = window
		self.color = color
		self.x = x
		self.y = y
		self.length = length
		self.width = width
		# self.rect = [self.x, self.y, self.length, self.width]


	def draw(self):
		# if DEBUG:
		# 	print(self.x, self.y)
			# print(self.rect[0], self.rect[1])
		pygame.draw.rect(self.window, self.color, self.get_rect())

	def get_rect(self):
		return [self.x, self.y, self.width, self.length]

def set_window():
	pygame.init()

	window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
	pygame.display.set_caption("Event Test")
	pygame.key.set_repeat(100, FPS//2)
	return window


def check_events(objects):
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			if DEBUG:
				print("KEYDOWN event for key %s" % (event.key))
			
			if event.key == pygame.K_ESCAPE:
				sys.exit()

			if event.key in (pygame.K_w,pygame.K_UP):
				if objects[0].y - 5 >= 0:
					objects[0].y -= 5
				else:
					objects[0].y = 0

			if event.key in (pygame.K_a, pygame.K_LEFT):
				if objects[0].x - 5 >= 0:
					objects[0].x -= 5
				else:
					objects[0].x = 0

			if event.key in (pygame.K_s, pygame.K_DOWN):
				if objects[0].y + objects[0].length + 5 <= SCREEN_HEIGHT:
					objects[0].y += 5
				else:
					objects[0].y = SCREEN_HEIGHT - objects[0].length

			if event.key in (pygame.K_d, pygame.K_RIGHT):
				if objects[0].x + objects[0].width + 5 <= SCREEN_WIDTH:
					objects[0].x += 5
				else:
					objects[0].x = SCREEN_WIDTH - objects[0].width

		elif event.type == pygame.USEREVENT:
			print(event.code)


def update(objects):
	ev = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_w})
	# ev = pygame.event.Event(pygame.USEREVENT, {'code': 'this is a test.'})
	pygame.event.post(ev)



def render(window, objects):
	# clear window
	window.fill((0, 0, 0))

	# draw stuff
	for o in objects:
		try:
			o.draw()
		except AttributeError:
			print("object did not have a draw method.")

	# update window
	pygame.display.flip()

def center_box(box):
	box.x = SCREEN_WIDTH//2 - box.width//2
	box.y = SCREEN_HEIGHT//2 - box.length//2

def loop(window):
	clock = pygame.time.Clock()
	box = Box(window, WHITE, 0, 0, 50, 50)
	center_box(box)
	objects = [box,]

	if DEBUG:
		print("key repeat (ms): ", pygame.key.get_repeat())

	while True:
		clock.tick(FPS)
		check_events(objects)
		update(objects)
		render(window, objects)

def main():
	window = set_window()
	loop(window)


if __name__ == '__main__':
	main()
