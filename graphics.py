import pygame

# globals
DEBUG = False # set to False before submission!

class shapes:
    square = "square"
    rectangle = "rectangle"
    tee = "tee"
    leftz = "leftz"
    rightz = "rightz"
    leftl = "leftl"
    rightl = "rightl"
    
    @staticmethod
    def get_shapes():
        '''Returns a tuple containing all of the shape types to be randomly selected for new shape spawns'''
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
    '''This is the general shape superclass used for all block objects'''
    def __init__(self, location, color, block_dim, window):
        self.location = location # location of "core block"
        self.color = color
        self.falling = True
        self.blocks = [] # each shape type will have unique list of locations for intrinsic blocks
        self.block_dim = block_dim
        self.orientation = 0 # orientation in degrees.

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
    def __init__(self, location, color, block_dim, window):
        super().__init__(location, color, block_dim, window)
        self.location = location
        self.color = color
        self.blocks = [ block([self.location[0], self.location[1]], color, block_dim, window), \
                        block([self.location[0] + block_dim, self.location[1]], color, block_dim, window), \
                        block([self.location[0] + 2*block_dim, self.location[1]], color, block_dim, window), \
                        block([self.location[0] - block_dim, self.location[1]], color, block_dim, window) ]

    ## Rectangle objects use distinct rotation instructions.

    # Updates the origin of rotation 
    def set_rotation_origin(self):
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
        # re-orient points to refer to top-left corner (needed for drawing)
        if self.orientation == 0:
            block.location[0] -= self.block_dim
        elif self.orientation == 90:
            block.location[0] -= self.block_dim

        elif self.orientation == 180:
            block.location[0] -= self.block_dim

        elif self.orientation == 270:
            block.location[0] -= self.block_dim        


    def rotate(self):
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
    def __init__(self, location, color, block_dim, window):
        super().__init__(location, color, block_dim, window)
        self.location = location
        self.color = color
        self.blocks = [ block([self.location[0], self.location[1]], color, block_dim, window), \
                        block([self.location[0] + block_dim, self.location[1]], color, block_dim, window), \
                        block([self.location[0] - block_dim, self.location[1]], color, block_dim, window), \
                        block([self.location[0], self.location[1] + block_dim], color, block_dim, window) ]


    def rotate(self):
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
    def __init__(self, location, color, block_dim, window):
        super().__init__(location, color, block_dim, window)
        self.location = location
        self.color = color
        self.blocks = [ block([self.location[0], self.location[1]], color, block_dim, window), \
                        block([self.location[0] + block_dim, self.location[1] + block_dim], color, block_dim, window), \
                        block([self.location[0] - block_dim, self.location[1]], color, block_dim, window), \
                        block([self.location[0], self.location[1] + block_dim], color, block_dim, window) ]

    def rotate(self):
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
    def __init__(self, location, color, block_dim, window):
        super().__init__(location, color, block_dim, window)
        self.location = location
        self.color = color
        self.blocks = [ block([self.location[0], self.location[1]], color, block_dim, window), \
                        block([self.location[0] + block_dim, self.location[1]], color, block_dim, window), \
                        block([self.location[0] - block_dim, self.location[1] + block_dim ], color, block_dim, window), \
                        block([self.location[0], self.location[1] + block_dim], color, block_dim, window) ]

    def rotate(self):
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
    def __init__(self, location, color, block_dim, window):
        super().__init__(location, color, block_dim, window)
        self.location = location
        self.color = color
        self.blocks = [ block([self.location[0], self.location[1] + block_dim], color, block_dim, window), \
                        block([self.location[0] + block_dim, self.location[1] + block_dim], color, block_dim, window), \
                        block([self.location[0] - block_dim, self.location[1] + block_dim ], color, block_dim, window), \
                        block([self.location[0] - block_dim, self.location[1]], color, block_dim, window) ]

    def rotate(self):
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
    def __init__(self, location, color, block_dim, window):
        super().__init__(location, color, block_dim, window)
        self.location = location
        self.color = color
        self.blocks = [ block([self.location[0] + block_dim, self.location[1]], color, block_dim, window), \
                        block([self.location[0] - block_dim, self.location[1] + block_dim], color, block_dim, window), \
                        block([self.location[0], self.location[1] + block_dim ], color, block_dim, window), \
                        block([self.location[0] + block_dim, self.location[1] + block_dim], color, block_dim, window) ]

    def rotate(self):
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
        pygame.draw.rect(window, self.color, (self.location[0], self.location[1], block_dim, block_dim))