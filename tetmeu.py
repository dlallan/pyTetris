import pygame, time


pygame.init()

TILE_SIZE = 40 # controls size of screen, shapes, etc.
NUM_TILES_WIDE = 10
NUM_TILES_LONG = 20
X_MARGIN = 1
Y_MARGIN = 1
SCREEN_WIDTH = TILE_SIZE * NUM_TILES_WIDE + X_MARGIN
SCREEN_HEIGHT = TILE_SIZE * NUM_TILES_LONG + Y_MARGIN
GRID_LINE_THICKNESS = 1
FPS = 50
black = (0, 0, 0)
white = (255, 255, 255)
gameDisplay = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

myfont = pygame.font.SysFont("monospace", 15)

START_LABEL_1 = myfont.render("Welcome to pytetris!", 1, (0,0,0))
START_LABEL_2 = myfont.render("Begin new game? (y/n):" , 1, (0,0,0))



def text_objects(text, font):
    textSurface = font.render(text, True, white)
    return textSurface, textSurface.get_rect()

def start_menu(display):

    display.fill(black)
    # Set window background
    display.blit(BackGround.image, BackGround.rect)
    
    largeText = pygame.font.Font('freesansbold.ttf',24)
    TextSurf1, TextRect1 = text_objects("Welcome to pytetris!", largeText)
    TextSurf2, TextRect2 = text_objects("Begin new game? (y/n):", largeText)

    TextRect1.center = ((SCREEN_WIDTH/2),(SCREEN_HEIGHT*0.4))
    TextRect2.center = ((SCREEN_WIDTH/2),(SCREEN_HEIGHT*0.6))

    display.blit(TextSurf1, TextRect1)

    display.blit(TextSurf2, TextRect2)


    pygame.display.update()
    wait_for_input = True
    while wait_for_input:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                print('hi')
                if event.key == pygame.K_y:
                    print('hey')
                    wait_for_input = False
                    new_game = False
        


                if event.key == pygame.K_n:
                    ygame.event.clear()
                    pygame.display.quit()
                    pygame.quit()

    return(new_game)
    

def pause_menu(gameDisplay):
    largeText = pygame.font.Font('freesansbold.ttf',115)
    TextSurf, TextRect = text_objects("Resume game? (y/n):", largeText)
    TextRect.center = ((SCREEN_WIDTH/2),(SCREEN_HEIGHT/2))
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: # rotate
                    wait_for_input = False





# initialize font; must be called after 'pygame.init()' to avoid 'Font not Initialized' error

# render text

