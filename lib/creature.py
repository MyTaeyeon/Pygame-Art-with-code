import pygame
import sys
import math
import copy
import random
import noise
import tree
import utilities as u
# import lib.utilities as u
# import lib.noise as noise
# import lib.tree as tree

pygame.init()

class simplePlayer:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.color = (255, 0, 0)
        self.jumping = False
        self.falling = False
        self.jumpy = 0
    
    def draw(self, surface):
        u.circle(surface, self.color, [self.x, self.y], 10)
    
    def update(self, onland):
        if self.falling == True:
            if self.y < onland:
                self.y += 3
            else:
                self.y = onland
                self.falling = False
            return
        if self.jumping == True:
            if self.y > self.jumpy:
                self.y -= 5
            else:
                self.y = self.jumpy
                self.jumping = False
                self.falling = True
            return
        self.y = onland
        return
        

class animal():
    def __init__(self) -> None:
        pass

    def __str__(self) -> str:
        pass

if __name__ == "__main__":
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()