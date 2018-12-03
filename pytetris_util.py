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

# Text
FONT = 'freesansbold.ttf'
FONT_SIZE_LARGE = 24
FONT_SIZE_MEDIUM = 20
# START_LABEL_1 = FONT.render("Welcome to pytetris!", 1, (0,0,0))
# START_LABEL_2 = FONT.render("Begin new game? (y/n):" , 1, (0,0,0))

# drop speed of shapes (ms)
EASY = 750
MEDIUM = 300
HARD = 150
DIFFICULTIES = [EASY, MEDIUM, HARD]
DIFFICULTY_CHANGE_THRESHOLD = 1*SCORE_MULTIPLIER # increase difficulty every n rows cleared

# Arduino config
SERIAL_PORT = '/dev/ttyACM0'
BAUD_RATE = 9600

# Create instance of Background sprite
BackGround = graphics.Background('tetrisb.jpg', [0,0])

# menu helpers
def text_objects(text, font):
    text_surface = font.render(text, True, WHITE)
    return text_surface, text_surface.get_rect()


def game_over_menu(game):
    
    # Set window background
    game.window.blit(BackGround.image, BackGround.rect)

    large_text = pygame.font.Font(FONT,FONT_SIZE_LARGE)
    text_surf_1, text_rect_1 = text_objects("Game Over. Player score: %s" % (game.player_score), large_text)
    text_surf_2, text_rect_2 = text_objects("Return to Start Menu? (y/n)", large_text)

    draw_centered_msg(game, text_surf_1, text_rect_1, text_surf_2, text_rect_2)

    wait_for_input = True
    start_menu = False
    while wait_for_input:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:  # start game
                    wait_for_input = False
                    start_menu = True
        
                elif event.key == pygame.K_n:  # exit
                    # quit_game()
                    wait_for_input = False

    return start_menu


def start_menu(game):

    # Set window background
    game.window.blit(BackGround.image, BackGround.rect)

    large_text = pygame.font.Font(FONT,FONT_SIZE_LARGE)
    text_surf_1, text_rect_1 = text_objects("Welcome to pytetris!", large_text)
    text_surf_2, text_rect_2 = text_objects("Begin new game? (y/n)", large_text)

    draw_centered_msg(game, text_surf_1, text_rect_1, text_surf_2, text_rect_2)

    wait_for_input = True
    new_game = False
    while wait_for_input:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:  # start game
                    wait_for_input = False
                    new_game = True
        
                elif event.key == pygame.K_n:  # exit
                    quit_game()
                    wait_for_input = False

    return new_game


def pause_menu(game):
    med_text = pygame.font.Font(FONT,FONT_SIZE_MEDIUM)
    text_surf_1, text_rect_1 = text_objects("Game Paused.", med_text)
    text_surf_2, text_rect_2 = text_objects("Esc: Resume  Q: Quit game", med_text)

    draw_centered_msg(game, text_surf_1, text_rect_1, text_surf_2, text_rect_2)

    wait_for_input = True
    while wait_for_input:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: # Resume game
                    wait_for_input = False

                elif event.key == pygame.K_q:
                    wait_for_input = False
                    quit_game(game)


def draw_centered_msg(game, text_surf_1, text_rect_1, text_surf_2, text_rect_2):
    # center text on screen
    text_rect_1.center = ((SCREEN_WIDTH/2),(SCREEN_HEIGHT*0.325))
    text_rect_2.center = ((SCREEN_WIDTH/2),(SCREEN_HEIGHT*0.525))
    
    # show message
    game.window.blit(text_surf_1, text_rect_1)
    game.window.blit(text_surf_2, text_rect_2)
    pygame.display.update()    


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
    global DIFFICULTIES

    pygame.init()
    pygame.key.set_repeat(100, FPS)  # enable key repeats every half a frame
    
    game = Game(pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)),
        TILE_SIZE, NUM_TILES_WIDE, NUM_TILES_LONG, pygame.time.Clock())
    
    update_score_display(game)
    
    # start at lowest difficulty i.e. the speed shapes move down
    DIFFICULTIES = [EASY, MEDIUM, HARD] # set in case of new game
    set_move_down_event(DIFFICULTIES.pop(0), game)

    return game


# update helpers
def update(game):
    # if there's no shape, spawn a new one
    if not check_for_active_shape(game):
        game.spawn_new_shape()

        # test if new shape has nowhere to go
        if check_for_game_over(game):
            game.game_over = True
            # else:
            #     print ("Quit game")
            #     quit_game(game)

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
        # pause_game(game)
        pause_menu(game)

    if event.key in (pygame.K_w,pygame.K_UP): # rotate
        try_rotate(game)

    if event.key in (pygame.K_a, pygame.K_LEFT): # move left
        try_move_left(game)

    if event.key in (pygame.K_s, pygame.K_DOWN): # move down
        try_move_down(game)

    if event.key in (pygame.K_d, pygame.K_RIGHT): # move right
        try_move_right(game)


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
        revert_orientation(game)

def revert_orientation(game):
    game.active_shape.orientation += 270 # -90 is equivalent to +270 rotation
    game.active_shape.orientation %= 360


# render helpers
def render(game):
    if pygame.display.get_init() and game.window:
        clear_window(game)
        draw_objects(game)
        draw_grid(game)
        update_score_display(game)

        # update frame
        pygame.display.flip()


def clear_window(game):
    # clear window
    game.window.fill(Game.backgroundColor)
    # Set window background
    game.window.blit(BackGround.image, BackGround.rect)

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
