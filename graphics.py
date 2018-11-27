import pygame

class shape:
    def __init__(self, location, color, block_dim, window):
        self.location = location
        self.color = color
    def draw(self):
        pygame.draw.rect(window, self.color, (self.location[0], self.location[1], 30, 30))

class square(shape):
    def __init__(self, location, color, block_dim, window):
        self.location = location
        self.color = color
        self.blocks = [[self.location[0], self.location[1]], [self.location[0] + block_dim, self.location[1]], 
        [self.location[0] + block_dim, self.location[1] + block_dim], [self.location[0], self.location[1] + block_dim]]
        self.height = block_dim * 2


    # Rotation does not effect square shapes
    def rotate(self):
        pass

    def draw(self, window):
        for block in self.blocks:
            pygame.draw.rect(window, self.color, (block[0], block[1], 30, 30))

class rectangle(shape):
    def __init__(self, location, color, block_dim, window):
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

    def draw(self, window):
        for block in self.blocks:
            pygame.draw.rect(window, self.color, (block[0], block[1], 30, 30))


class tee(shape):
    def __init__(self, location, color, block_dim, window):
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

    def draw(self, window):
        for block in self.blocks:
            pygame.draw.rect(window, self.color, (block[0], block[1], 30, 30))

class leftz(shape):
    def __init__(self, location, color, block_dim, window):
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

    def draw(self, window):
        for block in self.blocks:
            pygame.draw.rect(window, self.color, (block[0], block[1], 30, 30))


class rightz(shape):
    def __init__(self, location, color, block_dim, window):
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

    def draw(self, window):
        for block in self.blocks:
            pygame.draw.rect(window, self.color, (block[0], block[1], 30, 30))

class leftl(shape):
    def __init__(self, location, color, block_dim, window):
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

    def draw(self, window):
        for block in self.blocks:
            pygame.draw.rect(window, self.color, (block[0], block[1], 30, 30))

class rightl(shape):
    def __init__(self, location, color, block_dim, window):
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

    def draw(self, window):
        for block in self.blocks:
            pygame.draw.rect(window, self.color, (block[0], block[1], 30, 30))