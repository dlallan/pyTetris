import pygame, threading, time

# Globals
DEBUG = True

# Arduino config
SERIAL_PORT = '/dev/ttyACM0'
BAUD_RATE = 9600
PIN_RIGHT = 6
PIN_DOWN = 7
PIN_UP = 8
PIN_LEFT = 9
PINS = [PIN_RIGHT, PIN_DOWN, PIN_UP, PIN_LEFT]
NUM_PIN_STATE = 8

# TEST_ser_thread = threading.Thread(target=ser,_worker, args=[game.serial_port])
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

	@staticmethod
	def ser_worker(serial_port):
		t = threading.currentThread()  # need to check if parent thread modified t.stop
		if DEBUG:
			print("serial_port arg:", serial_port)
		while(not t.stop):
			pinStates = t.poll_serial(serial_port)
			# if DEBUG:
			# 	print(pinStates)
			if pinStates is None:
				if DEBUG:
					print("pinStates was empty")
				pass
			else:	
				pass
				# if DEBUG:
				# 	print(pinStates)

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
			t = threading.currentThread()  # need to check if parent thread modified t.stop

			time.sleep(1/FPS)  # keep thread from pinning
		if DEBUG:
			print("Exiting worker thread...")


	def poll_serial(self, serial_port):
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
