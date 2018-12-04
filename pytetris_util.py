'''
----------------------------------------------------------
Name: Dillon Allan, Ian Yurychuk
ID: 1350542, 1552809
CMPUT 274, Fall 2018

Final Project: pytetris - Python implementation of Tetris
----------------------------------------------------------
The file pytetris_util.py contains utility functions for 
pytetris.py.

Refer to the README for more information.
'''

import graphics, sys, pygame
from game import Game


# globals
DEBUG = False  # set to False before submission!

TILE_SIZE = 40 # controls size of screen, shapes, etc.
NUM_TILES_WIDE = 10
NUM_TILES_LONG = 20
X_MARGIN = 1
Y_MARGIN = 1
SCREEN_WIDTH = TILE_SIZE * NUM_TILES_WIDE + X_MARGIN
SCREEN_HEIGHT = TILE_SIZE * NUM_TILES_LONG + Y_MARGIN
GRID_LINE_THICKNESS = 1
FPS = 50

# colors
BLACK = 0, 0, 0
WHITE = 255, 255, 255


# Text
FONT = 'freesansbold.ttf'
FONT_SIZE_LARGE = 24
FONT_SIZE_MEDIUM = 20

# difficulty determined by drop speed of shapes (in ms)
EASY = 750
MEDIUM = 300
HARD = 150
DIFFICULTIES = [EASY, MEDIUM, HARD]

SCORE_MULTIPLIER = 10
DIFFICULTY_CHANGE_THRESHOLD = 100 # increase difficulty every n points earned

# Arduino config (EXPERIMENTAL -- NOT USED IN FINAL SUBMISSION)
SERIAL_PORT = '/dev/ttyACM0'
BAUD_RATE = 9600

# Create instance of Background image
BACKGROUND = graphics.Background('tetrisbg.jpg', [0,0])

# menu helpers
def text_objects(text, font):
    '''Get surface and rectangle dimensions for a given text and font.'''
    text_surface = font.render(text, True, WHITE)
    return text_surface, text_surface.get_rect()


def game_over_menu(game):
    '''Display Game Over menu to user and let them choose if they want to
    go back to the Start Menu or not.'''
    large_text = pygame.font.Font(FONT,FONT_SIZE_LARGE)
    text_surf_1, text_rect_1 = text_objects("Game Over. Player score: %s" % (game.player_score), large_text)
    text_surf_2, text_rect_2 = text_objects("Return to Start Menu? (y/n)", large_text)

    draw_centered_msg(game, text_surf_1, text_rect_1, text_surf_2, text_rect_2)

    
    # Have user use keyboard to choose to return to Start Menu or quit.
    wait_for_input = True
    start_menu = False
    while wait_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game(game)
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:  # start game
                    wait_for_input = False
                    start_menu = True
        
                elif event.key == pygame.K_n:  # exit
                    wait_for_input = False

            else:
                pygame.event.pump()

    return start_menu


def start_menu(game):
    '''Show Start Menu to user and let them choose if they want
    to start a new game or not.'''

    # Set window background
    game.window.blit(BACKGROUND.image, BACKGROUND.rect)

    large_text = pygame.font.Font(FONT,FONT_SIZE_LARGE)
    text_surf_1, text_rect_1 = text_objects("Welcome to pytetris!", large_text)
    text_surf_2, text_rect_2 = text_objects("Begin new game? (y/n)", large_text)

    draw_centered_msg(game, text_surf_1, text_rect_1, text_surf_2, text_rect_2)

    '''Have user use keyboard to choose to begin playing or quit.'''
    wait_for_input = True
    new_game = False
    while wait_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game(game)
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:  # start game
                    wait_for_input = False
                    new_game = True
        
                elif event.key == pygame.K_n:  # exit
                    quit_game(game)
                    wait_for_input = False
            else:
                pygame.event.pump()

    return new_game


def pause_menu(game):
    '''Show Pause Menu to user and let them choose if they want
    to resume playing or quit.'''
    med_text = pygame.font.Font(FONT,FONT_SIZE_MEDIUM)
    text_surf_1, text_rect_1 = text_objects("Game Paused.", med_text)
    text_surf_2, text_rect_2 = text_objects("Esc: Resume  Q: Quit game", med_text)

    draw_centered_msg(game, text_surf_1, text_rect_1, text_surf_2, text_rect_2)

    '''Have user use keyboard to choose t0 resume game or quit'''
    wait_for_input = True
    while wait_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game(game)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Resume game
                    wait_for_input = False
                    game.paused = False

                elif event.key == pygame.K_q:  # quit
                    wait_for_input = False
                    quit_game(game)
            else:
                pygame.event.pump()


def draw_centered_msg(game, text_surf_1, text_rect_1, text_surf_2, text_rect_2):
    '''Draw two lines of text roughly centred in the pygame display.'''
    # center text on screen
    text_rect_1.center = ((SCREEN_WIDTH/2),(SCREEN_HEIGHT*0.325))
    text_rect_2.center = ((SCREEN_WIDTH/2),(SCREEN_HEIGHT*0.525))
    
    # show message
    game.window.blit(text_surf_1, text_rect_1)
    game.window.blit(text_surf_2, text_rect_2)
    pygame.display.update()    


def quit_game(game):
    '''Quit pygame and end the program.'''
    
    # EXPERIMENTAL
    #   print("trying to stop worker thread:", TEST_ser_thread)
    #   TEST_ser_thread.stop_worker_thread()

    game.game_over = True
    pygame.display.quit()
    pygame.quit()
    sys.exit(0)


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


# def print_welcome(msg):
#     print(msg)
#     return


# def get_player_ready(prompt):
#     ok = False
#     while not ok:
#         user_response = input(prompt)  # ask user if they're ready to play
#         begin, ok = validate_user_response(user_response)
#         if pygame.display.get_init():
#             pygame.event.pump() # prevent hanging due to pygame event queue from filling up
#     return begin


def exit_with_msg(msg):
    '''End program with closing message in the console.'''
    print(msg)
    pygame.quit()
    sys.exit(0)


def startup_tetris():
    '''Initialize pygame and main game object.'''
    global DIFFICULTIES

    pygame.init()
    pygame.key.set_repeat(100, FPS)  # enable key repeats every once per frame
    
    game = Game(pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)),
        TILE_SIZE, NUM_TILES_WIDE, NUM_TILES_LONG, pygame.time.Clock())
    
    update_score_display(game)
    
    # start at lowest difficulty i.e. the speed shapes move down
    DIFFICULTIES = [EASY, MEDIUM, HARD] # set in case of new game
    set_move_down_event(DIFFICULTIES.pop(0), game)

    return game


# update helpers
def update(game):
    '''Maintain state of main game object. Run once per frame.'''

    # if there's no shape, spawn a new one
    if not check_for_active_shape(game):
        game.spawn_new_shape()

        # test if new shape has nowhere to go
        if check_for_game_over(game):
            game.game_over = True

    # else there is a shape -- check if not falling
    else:
        if not game.active_shape.falling:
            # unpack active shape to grid and clear active shape
            if DEBUG:
                print("Unpacking active shape")
            game.unpack_active_shape()
            game.active_shape = None  # clear random shape

            # check for filled rows
            # if filled rows exist, clear them, drop above rows immediately,
            # update score, and check for difficulty increase
            num_filled_rows = game.try_drop_filled_rows()
            if num_filled_rows:
                prev_score = game.player_score
                update_score(game, num_filled_rows)

                # increase difficulty when new player score exceeds DIFFICULTY_CHANGE_THRESHOLD
                if game.player_score % DIFFICULTY_CHANGE_THRESHOLD == 0:
                    try_increase_difficulty(game)


def try_increase_difficulty(game):
    '''Attempts to increase difficulty. Does nothing if at max difficulty already.'''
    if len(DIFFICULTIES):
        if DEBUG:
            print("increasing difficulty...")
        set_move_down_event(DIFFICULTIES.pop(0), game)


def set_move_down_event(difficulty, game):
    '''Create or update the "move down" event with the given difficulty'''
    pygame.time.set_timer(game.move_down_event, difficulty)


def check_for_game_over(game):
    '''special case of collision detection when active shape is in starting location
    and has already collided with blocks in the grid.'''
    if game.check_for_collisions():
        return True

    return False


def check_for_active_shape(game):
    '''Returns None if active shape doesn't exist.
    This method is only here for readability.'''
    return game.active_shape


def update_score(game, n):
    '''Increase score using n rows cleared, and SCORE_MULTIPLIER.'''
    game.player_score += n*SCORE_MULTIPLIER


def update_score_display(game):
    '''Update window title bar with current player score.'''
    pygame.display.set_caption("pytetris | player score: %s" % (game.player_score))


# event helpers
def check_events(game):
    '''Handle pygame events. Run once per frame.'''

    # EXPERIMENTAL
    # global TEST_ser_thread
    # with LOCK:# TEST
    
    # handle each event in pygame event queue
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            quit_game(game)

        elif event.type == pygame.KEYDOWN:  # keyboard events
            handle_keydown_events(event, game)
        
        elif event.type == game.move_down_event:
            try_move_down(game)  # move shape down periodically

        else:
            pygame.event.pump() # let pygame process internal events


def handle_keydown_events(event, game):
    '''User control event handling. Uses WASD or arrow keys
    for shape movement.'''

    if DEBUG:
        print("KEYDOWN event for key %s" % (event.key))
        
    if event.key == pygame.K_ESCAPE:  # enter pause menu
        game.paused = True
        pause_menu(game)

    elif event.key in (pygame.K_w,pygame.K_UP): # rotate
        try_rotate(game)

    elif event.key in (pygame.K_a, pygame.K_LEFT): # move left
        try_move_left(game)

    elif event.key in (pygame.K_s, pygame.K_DOWN): # move down
        try_move_down(game)

    elif event.key in (pygame.K_d, pygame.K_RIGHT): # move right
        try_move_right(game)


def is_out_of_bounds(game):
    '''check if active shape's location is out of bounds'''
    locs = game.get_active_shape_block_locs()
    
    # check each block's location
    for x,y in locs:
        if x < 0 or x >= SCREEN_WIDTH - TILE_SIZE \
        or y < 0 or y >= SCREEN_HEIGHT - TILE_SIZE:
            return True

    return False


def revert_locs(locs, game):
    '''Restore active shape's location to a previous location.'''
    
    # revert each block
    for i in range(len(locs)):
        game.active_shape.blocks[i].location = locs[i]


def try_move_down(game):
    '''Try to move active shape down one unit.
    Does nothing if no active shape exists, or if the move
    is invalid.'''

    if not game.active_shape:
        return

    old_locs = game.copy_active_shape_block_locs()
    game.active_shape.move_down()

    # restore old location if new location is out of bounds or collides
    # with blocks in the grid.
    if is_out_of_bounds(game) or game.check_for_collisions():
        revert_locs(old_locs, game)
        game.active_shape.falling = False # shape can't move any further down
        game.unpack_active_shape() # transfer blocks to the grid


def try_move_left(game):
    '''Try to move active shape left one unit.
    Does nothing if no active shape exists, or if the move
    is invalid.'''

    if not game.active_shape:
        return

    old_locs = game.copy_active_shape_block_locs()
    game.active_shape.move_left()

    # restore old location if new location is out of bounds or collides
    # with blocks in the grid.
    if is_out_of_bounds(game) or game.check_for_collisions():
        revert_locs(old_locs, game)


def try_move_right(game):
    '''Try to move active shape right one unit.
    Does nothing if no active shape exists, or if the move
    is invalid.'''
    if not game.active_shape:
        return

    old_locs = game.copy_active_shape_block_locs()
    game.active_shape.move_right()

    # restore old location if new location is out of bounds or collides
    # with blocks in the grid.
    if is_out_of_bounds(game) or game.check_for_collisions():
        revert_locs(old_locs, game)


def try_rotate(game):
    '''Try to rotate active shape 90 degrees clockwise..
    Does nothing if no active shape exists, or if the rotation
    is invalid.'''
    if not game.active_shape:
        return

    old_locs = game.copy_active_shape_block_locs()
    game.active_shape.rotate()
    
    # restore old location if new location is out of bounds or collides
    # with blocks in the grid.
    if is_out_of_bounds(game) or game.check_for_collisions():
        revert_locs(old_locs, game)
        revert_orientation(game)


def revert_orientation(game):
    '''Resets a 90 clockwise rotation for the active shape.'''
    game.active_shape.orientation += 270 # +270 is equivalent to -90 degrees
    game.active_shape.orientation %= 360


# render helpers
def render(game):
    '''Draw graphics for the game, including background, active shape, grid, 
    and player score. Called once per frame.'''
    if pygame.display.get_init() and game.window:
        clear_window(game)
        draw_objects(game)
        draw_grid(game)
        update_score_display(game)

        # update frame
        pygame.display.flip()


def clear_window(game):
    '''Clear window by overwriting with background.'''
    game.window.blit(BACKGROUND.image, BACKGROUND.rect)


def draw_objects(game):
    '''Draw active shape and grid blocks to pygame display.'''
    if check_for_active_shape(game):
        game.active_shape.draw(game.window, TILE_SIZE)

    for x in range(len(game.grid)):
        for y in range(len(game.grid[x])):        
            if game.grid[x][y]:
                game.grid[x][y].draw(game.window, TILE_SIZE)


def draw_grid(game):
    '''Draw grid lines in pygame based on screen dimensions relative to tile size.'''
    for x in range(0, NUM_TILES_WIDE+1):
        start = (x*TILE_SIZE, 0)
        end = (x*TILE_SIZE, SCREEN_HEIGHT)
        pygame.draw.line(game.window, WHITE, start, end, GRID_LINE_THICKNESS)

    for y in range(0, NUM_TILES_LONG+1):
        start = (0, y*TILE_SIZE)
        end = (SCREEN_WIDTH, y*TILE_SIZE)
        pygame.draw.line(game.window, WHITE, start, end, GRID_LINE_THICKNESS)
