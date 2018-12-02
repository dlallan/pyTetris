'''
----------------------------------------------------------
Name: Dillon Allan, Ian Yurychuk
ID: 1350542, 1552809
CMPUT 274, Fall 2018

Final Project: pytetris - Python implementation of Tetris
----------------------------------------------------------
assignment.2.part.2.cpp contains the main logic for the Arduino Chat program in 
its final implementation. It references Arduino.h for setting up the Arduino 
for serial communication.  Paul Lu's "powmod.h" was referenced for computing 
modulo operations involving exponentiations between 32-bit numbers. The files 
"server.h" and "client.h" were used to decouple the client and server 
funcionalities from the main chat program, while only exposing simple "begin"
functions that allow the handshake process to begin on startup.

This file contains the program's main function, setup helpers, and chat helpers.
The program begins with a call to "setup", which initializes the connected Arduino
and its serial ports 0 and 3. Next, a 32-bit random private key is obtained using 
"generatePrivateKey", which is used to generate a public key with "powModFast".
"beginHandShake" is called, which causes the Arduino to enter either Client or
Server mode based on whether logical Low or High is read from digital pin 13.
Client and Server modes behave as specified in the state diagrams found at
https://eclass.srv.ualberta.ca/course/view.php?id=44895
In both cases, the other Arduino's public key is obtained, and used to generate
a shared secret key. The main chat program begins at this point, where the 
shared secret key is used as the first element in two cipher streams used in
the "send" and "receive" functions. The send and receive functions behave 
similarly to their predecessors in Part 1 of this assignment, but with the added
functionality of using "next_key" to replace the current cipher with a new cipher
after each write or read for added security.

To run the program properly, the Arduinos must have their Serial 3 pins 
connected (see Wiring Instructions in README) with a common ground, and both users
must run serial-mon-[their Arduino port no.] to begin a chat session.

Exit status
0: Program has ended.
'''

import pytetris_util

# globals
DEBUG = False  # set to False before demo and before submitting!


# game states
def game_over(game):
	print("Game over. Player score: %s" % (game.player_score))
	# start_new_game = pytetris_util.get_player_ready("Return to Start Menu? (y/n) ")
	
	# if start_new_game:
	# 	new_game()
	# else:
	pytetris_util.exit_with_msg("Exiting pytetris.")


# Returns
# None
def game_paused():
	if DEBUG:
		print("[DEBUG] Game paused.")

	# let user choose to resume game or quit
	resume = pytetris_util.get_player_ready("Resume game? (y: resume, n: quit game) ")
	if not resume:
		pytetris_util.exit_with_msg("Exiting pytetris.")
		

def main_game(game):
	if DEBUG:
		print("[DEBUG] Starting new game.")

	# run main loop for the game
	while not game.game_over:
		pytetris_util.render(game)
		pytetris_util.check_events(game)
		pytetris_util.update(game)
		
		if game.game_over:
			if pytetris_util.game_over_menu(game):
				game = pytetris_util.startup_tetris() # start a new game when program first runs
				if not pytetris_util.start_menu(game):    # show start menu dialog for user 
					game.game_over = True
	            	

		game.clock.tick(pytetris_util.FPS) # lock game speed to FPS


	game_over(game)


def new_game():
	pytetris_util.print_welcome("Welcome to pytetris!")
	begin = pytetris_util.get_player_ready("Begin new game? (y/n): ")  # ask user if they're ready to play

	if begin:
		game = pytetris_util.startup_tetris() # set up a new game object
		main_game(game)
	else:
		pytetris_util.exit_with_msg("Exiting pytetris.")	


def init_display():
	pygame.init()
	return pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

def main():
	game = pytetris_util.startup_tetris() # start a new game when program first runs
	if pytetris_util.start_menu(game): 	  # show start menu dialog for user 
		print("starting new game...")
		main_game(game)
	
	print("Exiting pytetris.")

	return


if __name__ == "__main__":
	main()
