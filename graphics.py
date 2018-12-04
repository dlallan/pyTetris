"""
----------------------------------------------------------
Name: Dillon Allan, Ian Yurychuk
ID: 1350542, 1552809
CMPUT 274, Fall 2018

Final Project: pytetris - Python implementation of Tetris
----------------------------------------------------------
The file game.py contains a single class Game, which is used to capture the state of 
pytetris during runtime. It contains attributes for tile size, screen width/height in 
tiles, clock, active shape, and grid, which tracks shapes when they stop falling. It 
contains methods that are used for spawning new active shapes, "unpacking" the active 
shape into the grid, collision deteection, and dropping filled rows.

Refer to the README for more information.
"""
import pygame

# globals
DEBUG = False  # set to False before submission!

class shapes:
    '''Helper class for cataloging different types of shape.'''
    square = "square"
    rectangle = "rectangle"
    tee = "tee"
    leftz = "leftz"
    rightz = "rightz"
    leftl = "leftl"
    rightl = "rightl"
    
    @staticmethod
    def get_shapes():
        '''Returns a tuple containing all of the shape types.'''
        return  shapes.square, shapes.rectangle,\
                shapes.tee, shapes.leftz, shapes.rightz,\
                shapes.leftl, shapes.rightl


class Background(pygame.sprite.Sprite):
    '''This class loads a background image into a pygame sprite'''
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


class shape:
    '''Base class used for all types of shape objects'''
    def __init__(self, location, color, block_dim, window):
        self.location = location # location of "core block"
        self.color = color
        self.falling = True
        self.blocks = []            # each shape is made up of a collection of blocks.
        self.block_dim = block_dim
        self.orientation = 0        # orientation in degrees.

    def move_down(self):
        '''Generic move down instructions for each block object'''
        self.location[1] += self.block_dim  # update "core block" location
        for b in self.blocks:
            b.location[1] += self.block_dim

    def move_left(self):
        '''Generic move left instructions for each block object'''
        self.location[0] -= self.block_dim  # update "core block" location
        for b in self.blocks:
            b.location[0] -= self.block_dim

    def move_right(self):
        '''Generic move right instructions for each block object'''
        self.location[0] += self.block_dim  # update "core block" location
        for b in self.blocks:
            b.location[0] += self.block_dim

    def update_orientation(self):
        ''' update orientation in degrees assuming 90 degree rotation clockwise.'''
        self.orientation += 90 
        self.orientation %= 360

    def draw(self, window, block_dim):
        '''Generic draw instructions for all block objects'''
        for block in self.blocks:
            pygame.draw.rect(window, self.color, (block.location[0], block.location[1], block_dim, block_dim))


class square(shape):
    '''A two-by-two square made of blocks.'''
    def __init__(self, location, color, block_dim, window):
        super().__init__(location, color, block_dim, window)
        self.blocks = [ block([self.location[0], self.location[1]], color, block_dim, window), \
                        block([self.location[0] + block_dim, self.location[1]], color, block_dim, window), \
                        block([self.location[0] + block_dim, self.location[1] + block_dim],color, block_dim, window), \
                        block([self.location[0], self.location[1] + block_dim],color, block_dim, window) ]

    # Rotation does not affect square shapes
    def rotate(self):
        pass
            

class rectangle(shape):
    '''Four-by-one rectangle of blocks.'''
    def __init__(self, location, color, block_dim, window):
        super().__init__(location, color, block_dim, window)
        self.location = location
        self.color = color
        self.blocks = [ block([self.location[0], self.location[1]], color, block_dim, window), \
                        block([self.location[0] + block_dim, self.location[1]], color, block_dim, window), \
                        block([self.location[0] + 2*block_dim, self.location[1]], color, block_dim, window), \
                        block([self.location[0] - block_dim, self.location[1]], color, block_dim, window) ]


    # NOTE: Rectangle objects use distinct rotation instructions. 
    # The other shapes don't need the extra rotation/translation steps.
    def set_rotation_origin(self):
        '''Updates the origin of rotation relative to the shape's orientation.'''
        relx, rely = 0, 0
        if self.orientation == 0:
            relx = self.blocks[1].location[0]
            rely = self.blocks[1].location[1] + self.block_dim
        elif self.orientation == 90:
            relx = self.blocks[1].location[0]
            rely = self.blocks[1].location[1]
        elif self.orientation == 180:
            relx = self.blocks[0].location[0]
            rely = self.blocks[0].location[1]
        elif self.orientation == 270:
            relx = self.blocks[0].location[0] + self.block_dim
            rely = self.blocks[0].location[1]

        return relx, rely


    def reorient_point(self, block):
        '''Re-orient points to refer to top-left corner (needed for drawing).'''
        if self.orientation == 0:
            block.location[0] -= self.block_dim
        elif self.orientation == 90:
            block.location[0] -= self.block_dim

        elif self.orientation == 180:
            block.location[0] -= self.block_dim

        elif self.orientation == 270:
            block.location[0] -= self.block_dim        


    def rotate(self):
        '''Performs fixed point 90-degree clockwise rotation about the shape's centre.'''
        relx, rely = self.set_rotation_origin()
        self.update_orientation()

        # compute new block locations after one rotation
        for block in self.blocks:
            x = block.location[0] - relx
            y = block.location[1] - rely
            x1 = -y
            y1 = x
            block.location[0] = x1 + relx
            block.location[1] = y1 + rely
            
            self.reorient_point(block)


class tee(shape):
    '''Shape made of four blocks in a tee formation.'''
    def __init__(self, location, color, block_dim, window):
        super().__init__(location, color, block_dim, window)
        self.location = location
        self.color = color
        self.blocks = [ block([self.location[0], self.location[1]], color, block_dim, window), \
                        block([self.location[0] + block_dim, self.location[1]], color, block_dim, window), \
                        block([self.location[0] - block_dim, self.location[1]], color, block_dim, window), \
                        block([self.location[0], self.location[1] + block_dim], color, block_dim, window) ]


    def rotate(self):
        '''Performs fixed point 90-degree clockwise rotation about the shape's centre.'''
        relx = self.blocks[0].location[0]
        rely = self.blocks[0].location[1]
        for block in self.blocks:
            x = block.location[0] - relx
            y = block.location[1] - rely
            x1 = -y
            y1 = x
            block.location[0] = x1 + relx
            block.location[1] = y1 + rely


class leftz(shape):
    '''Shape made of four blocks in a left-hand Z formation.'''
    def __init__(self, location, color, block_dim, window):
        super().__init__(location, color, block_dim, window)
        self.location = location
        self.color = color
        self.blocks = [ block([self.location[0], self.location[1]], color, block_dim, window), \
                        block([self.location[0] + block_dim, self.location[1] + block_dim], color, block_dim, window), \
                        block([self.location[0] - block_dim, self.location[1]], color, block_dim, window), \
                        block([self.location[0], self.location[1] + block_dim], color, block_dim, window) ]

    def rotate(self):
        '''Performs fixed point 90-degree clockwise rotation about the shape's centre.'''
        relx = self.blocks[0].location[0]
        rely = self.blocks[0].location[1]
        for block in self.blocks:
            x = block.location[0] - relx
            y = block.location[1] - rely
            x1 = -y
            y1 = x
            block.location[0] = x1 + relx
            block.location[1] = y1 + rely


class rightz(shape):
    '''Shape made of four blocks in a right-hand Z formation.'''
    def __init__(self, location, color, block_dim, window):
        super().__init__(location, color, block_dim, window)
        self.location = location
        self.color = color
        self.blocks = [ block([self.location[0], self.location[1]], color, block_dim, window), \
                        block([self.location[0] + block_dim, self.location[1]], color, block_dim, window), \
                        block([self.location[0] - block_dim, self.location[1] + block_dim ], color, block_dim, window), \
                        block([self.location[0], self.location[1] + block_dim], color, block_dim, window) ]

    def rotate(self):
        '''Performs fixed point 90-degree clockwise rotation about the shape's centre.'''
        relx = self.blocks[0].location[0]
        rely = self.blocks[0].location[1]
        for block in self.blocks:
            x = block.location[0] - relx
            y = block.location[1] - rely
            x1 = -y
            y1 = x
            block.location[0] = x1 + relx
            block.location[1] = y1 + rely


class leftl(shape):
    '''Shape made of four blocks in a left-hand L formation.'''
    def __init__(self, location, color, block_dim, window):
        super().__init__(location, color, block_dim, window)
        self.location = location
        self.color = color
        self.blocks = [ block([self.location[0], self.location[1] + block_dim], color, block_dim, window), \
                        block([self.location[0] + block_dim, self.location[1] + block_dim], color, block_dim, window), \
                        block([self.location[0] - block_dim, self.location[1] + block_dim ], color, block_dim, window), \
                        block([self.location[0] - block_dim, self.location[1]], color, block_dim, window) ]

    def rotate(self):
        '''Performs fixed point 90-degree clockwise rotation about the shape's centre.'''
        relx = self.blocks[0].location[0]
        rely = self.blocks[0].location[1]
        for block in self.blocks:
            x = block.location[0] - relx
            y = block.location[1] - rely
            x1 = -y
            y1 = x
            block.location[0] = x1 + relx
            block.location[1] = y1 + rely


class rightl(shape):
    '''Shape made of four blocks in a right-hand L formation.'''    
    def __init__(self, location, color, block_dim, window):
        super().__init__(location, color, block_dim, window)
        self.location = location
        self.color = color
        self.blocks = [ block([self.location[0] + block_dim, self.location[1]], color, block_dim, window), \
                        block([self.location[0] - block_dim, self.location[1] + block_dim], color, block_dim, window), \
                        block([self.location[0], self.location[1] + block_dim ], color, block_dim, window), \
                        block([self.location[0] + block_dim, self.location[1] + block_dim], color, block_dim, window) ]

    def rotate(self):
        '''Performs fixed point 90-degree clockwise rotation about the shape's centre.'''
        relx = self.blocks[2].location[0]
        rely = self.blocks[2].location[1]
        for block in self.blocks:
            x = block.location[0] - relx
            y = block.location[1] - rely
            x1 = -y
            y1 = x
            block.location[0] = x1 + relx
            block.location[1] = y1 + rely


class block(shape):
    '''General object for a single block, used to fill grid space and construct shape types'''
    def __init__(self, location, color, block_dim, window):
        self.location = location
        self.color = color
        self.block_dim = block_dim

    def draw(self, window, block_dim):
        '''Render block to pygame display.'''
        pygame.draw.rect(window, self.color, (self.location[0], self.location[1], block_dim, block_dim))
