# <add info header here>

import graphics, sys, pygame 
from game import Game


#globals
DEBUG = False  # set to True before submission!

TILE_SIZE = 40 # controls size of screen, shapes, etc.
NUM_TILES_WIDE = 10
NUM_TILES_LONG = 20
X_MARGIN = 1
Y_MARGIN = 1
SCREEN_WIDTH = TILE_SIZE * NUM_TILES_WIDE + X_MARGIN
SCREEN_HEIGHT = TILE_SIZE * NUM_TILES_LONG + Y_MARGIN
GRID_LINE_THICKNESS = 1
FPS = 50

BLACK = 0, 0, 0
WHITE = 255, 255, 255

SCORE_MULTIPLIER = 10

# drop speed of shapes (ms)
EASY = 750
MEDIUM = 300
HARD = 150
DIFFICULTIES = [EASY, MEDIUM, HARD]
DIFFICULTY_CHANGE_THRESHOLD = 1*SCORE_MULTIPLIER # increase difficulty every n rows cleared

# Arduino config
SERIAL_PORT = '/dev/ttyACM0'
BAUD_RATE = 9600


# menu helpers
def quit_game(game):
    #   print("trying to stop worker thread:", TEST_ser_thread)
    #   TEST_ser_thread.stop_worker_thread()
    #   # TEST_ser_thread.stop = True
    #   # TEST_ser_thread.join()
    #   sys.exit()
    game.game_over = True
    pygame.event.clear()
    pygame.display.quit()
    pygame.quit()


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


def print_welcome(msg):
    print(msg)
    return


def get_player_ready(prompt):
    ok = False
    while not ok:
        user_response = input(prompt)  # ask user if they're ready to play
        begin, ok = validate_user_response(user_response)
        if pygame.display.get_init():
            pygame.event.pump() # prevent hanging due to pygame event queue from filling up
    return begin


def exit_with_msg(msg):
    print(msg)
    sys.exit()


def startup_tetris():
    # global TEST_ser_thread

    pygame.init()
    pygame.key.set_repeat(100, FPS//2)  # enable key repeats every half a frame
    
    # ser = None 
    # try: 
    #   ser = serial.Serial(SERIAL_PORT, BAUD_RATE)
    # except:
    #   print("[DEBUG] startup: Couldn't connect to serial port", SERIAL_PORT)
    #   pass

    game = Game(pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)),
        TILE_SIZE, NUM_TILES_WIDE, NUM_TILES_LONG, pygame.time.Clock())
    
    update_score_display(game)
    
    # start at lowest difficulty i.e. the speed shapes move down
    DIFFICULTIES = [EASY, MEDIUM, HARD] # set in case of new game
    set_move_down_event(DIFFICULTIES.pop(0), game)

    # TEST_ser_thread = WorkerThread(ser_worker, game.serial_port)
    # TEST_ser_thread.start()

    return game


# update helpers
def update(game):
    # if there's no shape, spawn a new one
    if not check_for_active_shape(game):
        game.spawn_new_shape()

        # test if new shape has nowhere to go
        if check_for_game_over(game):
            quit_game(game)

    # else there is a shape -- check if not falling
    else:
        if not game.active_shape.falling:
            # if not falling, check for game over cnd
            # if check_for_game_over(game):
            #     quit_game(game)

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
                update_score(game, num_filled_rows)


                # increase difficulty every n rows cleared where n = DIFFICULTY_CHANGE_THRESHOLD
                if num_filled_rows * SCORE_MULTIPLIER >= DIFFICULTY_CHANGE_THRESHOLD:
                    try_increase_difficulty(game)


def try_increase_difficulty(game):
    if len(DIFFICULTIES):
        print("increasing difficulty...")
        set_move_down_event(DIFFICULTIES.pop(0), game)


# Description
# Create or replace the custom event with the given difficulty
def set_move_down_event(difficulty, game):
    pygame.time.set_timer(game.move_down_event, difficulty)


def check_for_game_over(game):
    # special case of collision detection when active shape is in starting location
    # and has already collided with blocks in the grid.
    if game.check_for_collisions():
        return True

    return False


def check_for_active_shape(game):
    return game.active_shape


def update_score(game, n):
    game.player_score += n*SCORE_MULTIPLIER


def update_score_display(game):
    pygame.display.set_caption("pytetris | player score: %s" % (game.player_score))


# event helpers
def check_events(game):
    # global TEST_ser_thread
    # with LOCK:# TEST
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            quit_game(game)

        elif event.type == pygame.KEYDOWN:
            handle_keydown_events(event, game)
        
        elif event.type == game.move_down_event:
            try_move_down(game) # move shape down periodically

        else:
            pygame.event.pump() # let pygame process internal events


def handle_keydown_events(event, game):
    if DEBUG:
        print("KEYDOWN event for key %s" % (event.key))
        
    if event.key == pygame.K_ESCAPE: # enter pause menu
        # TEST_ser_thread.stop_worker_thread()
        # sys.exit()
        pause_game(game)

    if event.key in (pygame.K_w,pygame.K_UP): # rotate
        try_rotate(game)

    if event.key in (pygame.K_a, pygame.K_LEFT): # move left
        try_move_left(game)

    if event.key in (pygame.K_s, pygame.K_DOWN): # move down
        try_move_down(game)

    if event.key in (pygame.K_d, pygame.K_RIGHT): # move right
        try_move_right(game)

    # elif event.type == pygame.USEREVENT: # TEST
    #   print(event.code)


def pause_game(game):
    game.paused = True
    while game.paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.paused = False
                quit_game(game)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                game.paused = False
            else:
                pygame.event.pump()


def is_out_of_bounds(game):
    # check if active shape's location is out of bounds
    locs = game.get_active_shape_block_locs()
    # print(locs)
    for x,y in locs:
        # print (x, y)
        if x < 0 or x >= SCREEN_WIDTH - TILE_SIZE \
        or y < 0 or y >= SCREEN_HEIGHT - TILE_SIZE:
            return True

    return False


def revert_locs(locs, game):
    for i in range(len(locs)):
        game.active_shape.blocks[i].location = locs[i]


def try_move_down(game):
    if not game.active_shape:
        return

    old_locs = game.copy_active_shape_block_locs()
    game.active_shape.move_down()
    if is_out_of_bounds(game) or game.check_for_collisions():
        revert_locs(old_locs, game)
        game.active_shape.falling = False # shape can't move any further down
        game.unpack_active_shape() # transfer blocks to the grid


def try_move_left(game):
    if not game.active_shape:
        return

    old_locs = game.copy_active_shape_block_locs()
    game.active_shape.move_left()
    if is_out_of_bounds(game) or game.check_for_collisions():
        revert_locs(old_locs, game)


def try_move_right(game):
    if not game.active_shape:
        return

    old_locs = game.copy_active_shape_block_locs()
    game.active_shape.move_right()
    if is_out_of_bounds(game) or game.check_for_collisions():
        revert_locs(old_locs, game)


def try_rotate(game):
    # TODO: fix skewed rotations
    if not game.active_shape:
        return

    old_locs = game.copy_active_shape_block_locs()
    game.active_shape.rotate()
    if is_out_of_bounds(game) or game.check_for_collisions():
        revert_locs(old_locs, game)


# render helpers
def render(game):
    clear_window(game)
    draw_objects(game)
    draw_grid(game)
    update_score_display(game)

    # update frame
    pygame.display.flip()


def clear_window(game):
    # clear window
    game.window.fill(Game.backgroundColor)


def draw_objects(game):
    # draw stuff
    if check_for_active_shape(game):
        game.active_shape.draw(game.window, TILE_SIZE)

    for x in range(len(game.grid)):
        for y in range(len(game.grid[x])):        
            if game.grid[x][y]:
                game.grid[x][y].draw(game.window, TILE_SIZE)


def draw_grid(game):
    for x in range(0, NUM_TILES_WIDE+1):
        start = (x*TILE_SIZE, 0)
        end = (x*TILE_SIZE, SCREEN_HEIGHT)
        pygame.draw.line(game.window, WHITE, start, end, GRID_LINE_THICKNESS)

    for y in range(0, NUM_TILES_LONG+1):
        start = (0, y*TILE_SIZE)
        end = (SCREEN_WIDTH, y*TILE_SIZE)
        pygame.draw.line(game.window, WHITE, start, end, GRID_LINE_THICKNESS)
