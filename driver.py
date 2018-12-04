def ser_worker(serial_port):
	t = threading.currentThread()  # need to check if parent thread modified t.stop
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