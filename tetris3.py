import sys, pygame, time, graphics, random
from pygame.locals import *

# initialize pygame

pygame.init()

# initialize font; must be called after 'pygame.init()' to avoid 'Font not Initialized' error
myfont = pygame.font.SysFont("monospace", 15)

# render text
label = myfont.render("GAME OVER!", 1, (255,255,0))


white = (255,255,255)
black = (0,0,0)

red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
colors = [red, green, blue]

delay = 200
block_dim = 30

(width, height) = ((block_dim*10) + 1 , (block_dim*20) + 1)



start_location = ( (4 * block_dim, 0) )



# open window, load background

left_boundary = 0
right_boundary = width
yboundary = height - 31

gameDisplay = pygame.display.set_mode((width, height))
#bg = pygame.image.load("bg.png")
# Set title to the window
pygame.display.set_caption("Tatris")



move_down_event = pygame.USEREVENT+1
create_block_event = pygame.USEREVENT+2

end_game = False
create_block = pygame.event.Event(create_block_event)

pygame.time.set_timer(move_down_event, delay)

clock = pygame.time.Clock()

def move_down():
    for block in current_block.blocks:

        block[1] = block[1] + block_dim



grid = [[None] * 10] * 20

left_boundary = 0
right_boundary = width - 1
y_boundary = height - 1




def unpack(xloc, yloc, grid, block_dim, gameDisplay):
    location = [xloc, yloc - block_dim]
    grid.reverse()
    grid[int(yloc/block_dim - 1)][int((xloc/block_dim))] = graphics.block(location, current_block.color, block_dim, gameDisplay)
    grid.reverse()
    #print(grid)


def collide_y(current_block, grid, block_dim, gameDisplay, y_boundary):

    y_collision = False
    for block in current_block.blocks:
        if block[1] == y_boundary:
            collide_y = True
            pygame.event.post(create_block)
            for unblock in current_block.blocks:
                unpack(unblock[0], unblock[1], grid, block_dim, gameDisplay)
                print('Block unpacked')
            break
        print(block[0]/block_dim)
        print(block[1]/block_dim)
        if grid[int(block[1]/block_dim)][int(block[0]/block_dim)] != None:
            collide_y = True
            pygame.event.post(create_block)
            for block in current_block.blocks:
                unpack(block[0], block[1], grid, block_dim, gameDisplay)
            break


    return(y_collision)

newblocks = -1
blocks = []
running = True
while running:
    #clock.tick(delay)

    if end_game:
        gameDisplay.blit(label, (100, 100))
        time.sleep(2000)
    else:
        if newblocks == -1:
            pygame.event.post(create_block)

        # handle events
        for event in pygame.event.get():
            if event.type == create_block_event:
                current_block = (graphics.square(start_location, colors[(random.randint(1,3))-1], block_dim, gameDisplay))
                newblocks += 1
            if event.type == move_down_event:
                move_down()
                #left_collision = collide_left(current_block, grid)
                #right_collision = collide_right(current_block, grid)
                y_collision = collide_y(current_block, grid, block_dim, gameDisplay, y_boundary)

            if event.type == pygame.QUIT:
                running = False

    # update game state
    gameDisplay.fill(black)

    # draw grid



        #draw objects

    for row in grid:
        for space in row:
            if space != None:
                space.draw(gameDisplay, block_dim, space.location)
                #print(space.location)
    #print('hi')            
    current_block.draw(gameDisplay, block_dim)
    current_block.rotate()

    for a in range(0, 21):
        pygame.draw.line(gameDisplay, white, (0+(a*30),0), (0+(a*30), 810), 1)

    for a in range(0, 28):
        pygame.draw.line(gameDisplay, white, (0 ,0+(a*30)), (600, 0+(a*30)), 1)

    pygame.display.flip()
