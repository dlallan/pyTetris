import pygame
# block_dim = 30


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
        self.location = location
        self.color = color
        self.falling = True
    # def draw(self, block_dim):
    #     pygame.draw.rect(window, self.color, (self.location[0], self.location[1], block_dim, block_dim))

class square(shape):
    def __init__(self, location, color, block_dim, window):
        super().__init__(location, color, block_dim, window)
        # self.location = location
        # self.color = color
        self.blocks = [ block([self.location[0], self.location[1]], color, block_dim, window), \
                        block([self.location[0] + block_dim, self.location[1]], color, block_dim, window), \
                        block([self.location[0] + block_dim, self.location[1] + block_dim],color, block_dim, window), \
                        block([self.location[0], self.location[1] + block_dim],color, block_dim, window) ]
        self.height = block_dim * 2


    # Rotation does not effect square shapes
    def rotate(self):
        pass

    def draw(self, window, block_dim):
        for block in self.blocks:
            pygame.draw.rect(window, self.color, (block.location[0], block.location[1], block_dim, block_dim))
            

class rectangle(shape):
    def __init__(self, location, color, block_dim, window):
        super().__init__(location, color, block_dim, window)
        self.location = location
        self.color = color
        self.blocks = [[self.location[0], self.location[1]], [self.location[0] + block_dim, self.location[1]], 
        [self.location[0] + 2*block_dim, self.location[1]], [self.location[0] - block_dim, self.location[1]]]
        self.height = block_dim

    def rotate(self):
        relx = self.blocks[0][0]
        rely = self.blocks[0][1]
        for block in self.blocks:
            x = block[0] - relx
            y = block[1] - rely
            x1 = y
            y1 = -x
            block[0] = x1 + relx
            block[1] = y1 + rely

    def draw(self, window, block_dim):
        for block in self.blocks:
            pygame.draw.rect(window, self.color, (block[0], block[1], block_dim, block_dim))


class tee(shape):
    def __init__(self, location, color, block_dim, window):
        super().__init__(location, color, block_dim, window)
        self.location = location
        self.color = color
        self.blocks = [[self.location[0], self.location[1]], [self.location[0] + block_dim, self.location[1]], 
        [self.location[0] - block_dim, self.location[1]], [self.location[0], self.location[1] + block_dim]]
        self.height = block_dim * 2

    def rotate(self):
        relx = self.blocks[0][0]
        rely = self.blocks[0][1]
        for block in self.blocks:
            x = block[0] - relx
            y = block[1] - rely
            x1 = y
            y1 = -x
            block[0] = x1 + relx
            block[1] = y1 + rely

    def draw(self, window, block_dim):
        for block in self.blocks:
            pygame.draw.rect(window, self.color, (block[0], block[1], block_dim, block_dim))

class leftz(shape):
    def __init__(self, location, color, block_dim, window):
        super().__init__(location, color, block_dim, window)
        self.location = location
        self.color = color
        self.blocks = [[self.location[0], self.location[1]], [self.location[0] + block_dim, self.location[1] + block_dim], 
        [self.location[0] - block_dim, self.location[1]], [self.location[0], self.location[1] + block_dim]]
        self.height = block_dim * 2

    def rotate(self):
        relx = self.blocks[0][0]
        rely = self.blocks[0][1]
        for block in self.blocks:
            x = block[0] - relx
            y = block[1] - rely
            x1 = y
            y1 = -x
            block[0] = x1 + relx
            block[1] = y1 + rely

    def draw(self, window, block_dim):
        for block in self.blocks:
            pygame.draw.rect(window, self.color, (block[0], block[1], block_dim, block_dim))


class rightz(shape):
    def __init__(self, location, color, block_dim, window):
        super().__init__(location, color, block_dim, window)
        self.location = location
        self.color = color
        self.blocks = [[self.location[0], self.location[1]], [self.location[0] + block_dim, self.location[1]], 
        [self.location[0] - block_dim, self.location[1] + block_dim ], [self.location[0], self.location[1] + block_dim]]
        self.height = block_dim * 2

    def rotate(self):
        relx = self.blocks[0][0]
        rely = self.blocks[0][1]
        for block in self.blocks:
            x = block[0] - relx
            y = block[1] - rely
            x1 = y
            y1 = -x
            block[0] = x1 + relx
            block[1] = y1 + rely

    def draw(self, window, block_dim):
        for block in self.blocks:
            pygame.draw.rect(window, self.color, (block[0], block[1], block_dim, block_dim))

class leftl(shape):
    def __init__(self, location, color, block_dim, window):
        super().__init__(location, color, block_dim, window)
        self.location = location
        self.color = color
        self.blocks = [[self.location[0], self.location[1] + block_dim], [self.location[0] + block_dim, self.location[1] + block_dim], 
        [self.location[0] - block_dim, self.location[1] + block_dim ], [self.location[0] - block_dim, self.location[1]]]
        self.height = block_dim * 2

    def rotate(self):
        relx = self.blocks[0][0]
        rely = self.blocks[0][1]
        for block in self.blocks:
            x = block[0] - relx
            y = block[1] - rely
            x1 = y
            y1 = -x
            block[0] = x1 + relx
            block[1] = y1 + rely

    def draw(self, window, block_dim):
        for block in self.blocks:
            pygame.draw.rect(window, self.color, (block[0], block[1], block_dim, block_dim))

class rightl(shape):
    def __init__(self, location, color, block_dim, window):
        super().__init__(location, color, block_dim, window)
        self.location = location
        self.color = color
        self.blocks = [[self.location[0] + block_dim, self.location[1]], [self.location[0] - block_dim, self.location[1] + block_dim], 
        [self.location[0], self.location[1] + block_dim ], [self.location[0] + block_dim, self.location[1] + block_dim]]
        self.height = block_dim * 2

    def rotate(self):
        relx = self.blocks[0][0]
        rely = self.blocks[0][1]
        for block in self.blocks:
            x = block[0] - relx
            y = block[1] - rely
            x1 = y
            y1 = -x
            block[0] = x1 + relx
            block[1] = y1 + rely

    def draw(self, window, block_dim):
        for block in self.blocks:
            pygame.draw.rect(window, self.color, (block[0], block[1], block_dim, block_dim))

class block(shape):
    def __init__(self, location, color, block_dim, window):
        self.location = location
        self.color = color
    def draw(self, window, block_dim, location):
        pygame.draw.rect(window, self.color, (location[0], location[1], block_dim, block_dim))