from typing import Any
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
screen = pygame.display.set_mode([640, 320])
screen.fill((255, 255, 255))
class Arrow():
    def __init__(self, x, y, alpha, v) -> None:
        self.x = x
        self.y = y
        self.g = 1
        self.v = v
        self.alpha = alpha
        self.color = (150,150,150)
        self.time = 0
        self.c = ()

    def draw(self, surface):
        u.circle(surface, self.color, [self.x, self.y], 10)

    def update(self, onland):
        self.x += self.vx
        if self.ay == 0:
            self.y = onland
        else:
            self.stuckinSky = True
            self.time += 1
            self.y -= self.vy - int(self.ay * (2*self.time - 1) / 2)
            if self.y > onland:
                self.y = onland
                self.ay = 0
                self.stuckinSky = False

class simplePlayer:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.ay = 0
        self.vx = 0
        self.vy = 0
        self.color = (255, 0, 0)
        self.time = 0
        self.stuckinSky = False
    
    def draw(self, surface):
        u.circle(surface, self.color, [self.x, self.y], 10)
    
    def update(self, onland):
        self.x += self.vx
        if self.ay == 0:
            self.y = onland
        else:
            self.stuckinSky = True
            self.time += 1
            self.y -= self.vy - int(self.ay * (2*self.time - 1) / 2)
            if self.y > onland:
                self.y = onland
                self.ay = 0
                self.stuckinSky = False
        
if __name__ == "__main__":
    arrows = [Arrow(100, 100), Arrow(100, 150), Arrow(100, 200)]
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        # screen.fill((255, 255, 255))
        
        for x in arrows:
            x.draw(screen)
            x.fly()
        pygame.display.update()