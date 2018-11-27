# <put main program header here>

import pytetris_util

# globals
DEBUG = True  # set to False before demo and before submitting!





# game states
def game_over(game):
	print("Game over. Player score: %s" % (game.player_score))
	start_new_game = pytetris_util.get_player_ready("Start new game? (y/n) ")
	
	if start_new_game:
		new_game()
	else:
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
	while True:
		pytetris_util.check_events(game)
		pytetris_util.update(game)
		pytetris_util.render(game)
		
		game.clock.tick(FPS) # lock game speed to FPS


def new_game():
	pytetris_util.print_welcome("Welcome to pytetris!")
	begin = pytetris_util.get_player_ready("Begin new game? (y/n): ")  # ask user if they're ready to play

	if begin:
		game = pytetris_util.startup_tetris() # set up a new game object
		main_game(game)
	else:
		pytetris_util.exit_with_msg("Exiting pytetris.")	


def main():
	new_game()  # start a new game when program first runs
	return


if __name__ == "__main__":
	main()
