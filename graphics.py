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
        return  shapes.square, shapes.rectangle,\
                shapes.tee, shapes.leftz, shapes.rightz,\
                shapes.leftl, shapes.rightl


class shape:
    def __init__(self, location, color, block_dim, window):
        self.location = location # location of "core block"
        self.color = color
        self.falling = True
        self.blocks = []
        self.block_dim = block_dim
        self.orientation = 0 # orientation in degrees.

    def move_down(self):
        self.location[1] += self.block_dim  # update "core block" location
        for b in self.blocks:
            b.location[1] += self.block_dim

    def move_left(self):
        self.location[0] -= self.block_dim  # update "core block" location
        for b in self.blocks:
            b.location[0] -= self.block_dim

    def move_right(self):
        self.location[0] += self.block_dim  # update "core block" location
        for b in self.blocks:
            b.location[0] += self.block_dim

    def update_orientation(self):
        ''' update orientation in degrees assuming 90 degree rotation clockwise.'''
        self.orientation += 90 
        self.orientation %= 360

    def draw(self, window, block_dim):
        for block in self.blocks:
            pygame.draw.rect(window, self.color, (block.location[0], block.location[1], block_dim, block_dim))


class square(shape):
    def __init__(self, location, color, block_dim, window):
        super().__init__(location, color, block_dim, window)
        self.blocks = [ block([self.location[0], self.location[1]], color, block_dim, window), \
                        block([self.location[0] + block_dim, self.location[1]], color, block_dim, window), \
                        block([self.location[0] + block_dim, self.location[1] + block_dim],color, block_dim, window), \
                        block([self.location[0], self.location[1] + block_dim],color, block_dim, window) ]
        self.height = block_dim * 2

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
        self.height = block_dim * 2


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
        self.height = block_dim * 2

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
        self.height = block_dim * 2

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
        self.height = block_dim * 2

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
        self.height = block_dim * 2

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
    def __init__(self, location, color, block_dim, window):
        self.location = location
        self.color = color
        self.block_dim = block_dim

    def draw(self, window, block_dim):
        pygame.draw.rect(window, self.color, (self.location[0], self.location[1], block_dim, block_dim))